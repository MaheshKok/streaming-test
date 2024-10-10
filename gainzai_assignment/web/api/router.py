from fastapi.routing import APIRouter

from gainzai_assignment.web.api import (
    assistant,
    docs,
    dummy,
    echo,
    monitoring,
    redis,
    thread,
    users,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(assistant.router, prefix="/assistants", tags=["assistants"])
api_router.include_router(thread.router, prefix="/threads", tags=["threads"])
