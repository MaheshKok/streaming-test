# type: ignore
import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from gainzai_assignment.db.base import Base
from gainzai_assignment.db.dependencies import get_db_session, get_db_session_ws
from gainzai_assignment.settings import settings


class UserDbModel(SQLAlchemyBaseUserTableUUID, Base):
    """
    Represents a user entity.

    Inherits from SQLAlchemyBaseUserTableUUID to include:
    - id (UUID)
    - email (string, unique)
    - hashed_password (string)
    - is_active (bool)
    - is_superuser (bool)
    - is_verified (bool)
    """

    __tablename__ = "users"


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Represents a read command for a user."""


class UserCreate(schemas.BaseUserCreate):
    """Represents a create command for a user."""


class UserUpdate(schemas.BaseUserUpdate):
    """Represents an update command for a user."""


class UserManager(UUIDIDMixin, BaseUserManager[UserDbModel, uuid.UUID]):
    """Manages a user session and its tokens."""

    reset_password_token_secret = settings.users_secret
    verification_token_secret = settings.users_secret


async def get_user_db(
    session: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserDatabase:
    """
    Yield a SQLAlchemyUserDatabase instance.

    :param session: asynchronous SQLAlchemy session.
    :yields: instance of SQLAlchemyUserDatabase.
    """
    yield SQLAlchemyUserDatabase(session, UserDbModel)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> UserManager:
    """
    Yield a UserManager instance.

    :param user_db: SQLAlchemy user db instance
    :yields: an instance of UserManager.
    """
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    """
    Return a JWTStrategy in order to instantiate it dynamically.

    :returns: instance of JWTStrategy with provided settings.
    """
    return JWTStrategy(secret=settings.users_secret, lifetime_seconds=None)


async def get_user_db_ws() -> SQLAlchemyUserDatabase:
    """
    Yield a SQLAlchemyUserDatabase instance for WebSocket connections.

    :return: An instance of SQLAlchemyUserDatabase.
    """
    async for session in get_db_session_ws():
        yield SQLAlchemyUserDatabase(session, UserDbModel)


async def get_user_manager_ws(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db_ws),
) -> UserManager:
    """
    Yield a UserManager instance for WebSocket connections.

    :param user_db: SQLAlchemy user database instance.
    :return: An instance of UserManager.
    """
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_jwt = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
cookie_transport = CookieTransport()
auth_cookie = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

backends = [
    auth_cookie,
    auth_jwt,
]

api_users = FastAPIUsers[UserDbModel, uuid.UUID](get_user_manager, backends)

current_active_user = api_users.current_user(active=True)
