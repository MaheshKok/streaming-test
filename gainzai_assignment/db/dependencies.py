from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from gainzai_assignment.db.base import SessionLocal


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:
        yield session
    finally:
        await session.commit()
        await session.close()


async def get_db_session_ws() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a SQLAlchemy AsyncSession for WebSocket connections.

    :return: An instance of AsyncSession.
    """
    async with SessionLocal() as session:
        yield session
