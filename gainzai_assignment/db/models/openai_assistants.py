import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, String

from gainzai_assignment.db.base import Base


class OpenAIAssistantDbModel(Base):
    """OpenAI Assistant to save all the assistants created so that we can use it for future reference where we can use the same assistant id to continue the conversation"""

    __tablename__ = "openai_assistants"

    openai_assistant_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        index=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
    )
