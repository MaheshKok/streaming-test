import datetime

from pydantic import BaseModel, ConfigDict


class OpenAIThreadModelDTO(BaseModel):
    """
    DTO for openai thread models.

    It returned when accessing openai thread from the API.
    """

    openai_thread_id: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class OpenAIThreadModelInputDTO(BaseModel):
    """DTO for creating new openai thread model."""

    openai_thread_id: str
