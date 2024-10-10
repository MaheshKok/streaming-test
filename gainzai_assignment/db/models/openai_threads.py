import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, String

from gainzai_assignment.db.base import Base


class OpenAIThreadDbModel(Base):
    """OpenAI Thread to save all the threads created so that we can use it for future reference where we can use the same thread id to continue the conversation"""

    __tablename__ = "openai_threads"

    openai_thread_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
    )
