from typing import List

from fastapi import APIRouter, Depends
from openai import AsyncOpenAI

from gainzai_assignment.db.dao.openai_thread_dao import OpenAIThreadDAO
from gainzai_assignment.db.models.openai_threads import OpenAIThreadDbModel
from gainzai_assignment.settings import settings
from gainzai_assignment.web.api.thread.schema import OpenAIThreadModelDTO

router = APIRouter()


@router.get("/", response_model=List[OpenAIThreadModelDTO])
async def get_thread_models(
    limit: int = 10,
    offset: int = 0,
    openai_thread_dao: OpenAIThreadDAO = Depends(),
) -> List[OpenAIThreadDbModel]:
    """
    Retrieve all openai thread objects from the database.

    :param limit: limit of openai thread objects, defaults to 10.
    :param offset: offset of openai thread objects, defaults to 0.
    :param openai_thread_dao: DAO for openai thread models.
    :return: list of openai thread objects from database.
    """
    return await openai_thread_dao.get_all_openai_threads(limit=limit, offset=offset)


@router.post("/", response_model=OpenAIThreadModelDTO)
async def create_openai_thread_model(
    openai_thread_dao: OpenAIThreadDAO = Depends(),
):
    """
    Creates a new openai thread object in the database.

    :param openai_thread_dao: openai thread object to create.
    """
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    openai_thread_object = await client.beta.threads.create()
    return await openai_thread_dao.create_openai_thread_model(openai_thread_object.id)
