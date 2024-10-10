from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from gainzai_assignment.db.meta import meta
from gainzai_assignment.settings import settings

DATABASE_URL = str(settings.db_url)  # Ensure this is defined in your settings


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta


# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to False in production
)

# Create the async sessionmaker
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
