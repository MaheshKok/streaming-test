import logging
from pathlib import Path
from typing import List, NoReturn

from fastapi import APIRouter, Body, Depends, HTTPException, Query, WebSocket, status
from fastapi.exceptions import WebSocketException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi_users.authentication import JWTStrategy
from openai import AsyncOpenAI
from sqlalchemy.exc import SQLAlchemyError

from gainzai_assignment.db.dao.openai_assistant_dao import OpenAIAssistantDAO
from gainzai_assignment.db.dao.openai_thread_dao import OpenAIThreadDAO
from gainzai_assignment.db.dependencies import get_db_session_ws
from gainzai_assignment.db.models.openai_assistants import OpenAIAssistantDbModel
from gainzai_assignment.db.models.users import get_user_manager_ws  # type: ignore
from gainzai_assignment.db.models.users import UserRead, get_jwt_strategy

# from jose import JWTError
from gainzai_assignment.services.assistant.assistant import AssistantService
from gainzai_assignment.services.assistant.cache import thread_ws_connections
from gainzai_assignment.settings import settings
from gainzai_assignment.web.api.assistant.schema import OpenAIAssistantModelDTO

router = APIRouter()
logger = logging.getLogger("assistant_ws")

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def get_current_user(
    token: str = Query(...),
    jwt_strategy: JWTStrategy = Depends(get_jwt_strategy),
    user_manager=Depends(get_user_manager_ws),
) -> UserRead:
    """
    Authenticate the user by decoding the JWT token.

    :param token: JWT token from query parameters.
    :param jwt_strategy: JWTStrategy instance from FastAPI-Users.
    :return: Authenticated UserRead instance.
    :raises WebSocketException: If token is invalid or user does not exist.
    """
    try:
        logger.info("Decoding JWT token.")
        user = await jwt_strategy.read_token(
            token,
            user_manager=user_manager,
        )  # Correct method to decode JWT
        if user is None:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid authentication token.",
            )
        logger.info(f"Authenticated user: {user.email}")
        return user
    except Exception:
        logger.exception("JWT decoding failed.")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid authentication token.",
        )


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: UserRead = Depends(get_current_user),
    thread_id: str = Query(),
    assistant_id: str = Query(),
) -> None:
    """
    Websocket for AI Assistant responses.
    """
    logging.info("WebSocket endpoint started.")
    async for session in get_db_session_ws():
        assistant_dao = OpenAIAssistantDAO(session=session)
        assistant_db_models = await assistant_dao.filter(assistant_id)
        if not assistant_db_models:
            raise HTTPException(
                status_code=404,
                detail=f"Assistant: [ {assistant_id} ] not found.",
            )

        thread_dao = OpenAIThreadDAO(session=session)
        thread_db_models = await thread_dao.filter(thread_id)
        if not thread_db_models:
            raise HTTPException(
                status_code=404,
                detail=f"Thread: [ {thread_id} ] not found.",
            )

    await websocket.accept()
    logger.info(f"WebSocket connection accepted for user: {user.email}")

    # Add the WebSocket connection to the connections dictionary
    if thread_id not in thread_ws_connections:
        thread_ws_connections[thread_id] = []
    thread_ws_connections[thread_id].append(websocket)

    assistant_service = AssistantService(websocket, user, thread_id, assistant_id)
    try:
        await assistant_service.handle_messages()
    except WebSocketException:
        logger.exception("WebSocketException exception occurred.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except (SQLAlchemyError, Exception) as e:
        logger.exception(f"Unexpected error in WebSocket connection, error: {e!s}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)


@router.get("/ui", response_class=HTMLResponse)
async def get_assistant_ui() -> FileResponse:
    """
    Serve the AI Assistant frontend.
    """
    return FileResponse(
        Path(__file__).resolve().parent.parent.parent
        / "static"
        / "assistant_index.html",
    )


@router.get("/", response_model=List[OpenAIAssistantModelDTO])
async def get_assistant_models(
    limit: int = 10,
    offset: int = 0,
    openai_assistant_dao: OpenAIAssistantDAO = Depends(),
) -> List[OpenAIAssistantDbModel]:
    """
    Retrieve all openai assistant objects from the database.

    :param limit: limit of openai assistant objects, defaults to 10.
    :param offset: offset of openai assistant objects, defaults to 0.
    :param openai_assistant_dao: DAO for openai assistant models.
    :return: list of openai assistant objects from database.
    """
    return await openai_assistant_dao.get_all_openai_assistants(
        limit=limit,
        offset=offset,
    )
