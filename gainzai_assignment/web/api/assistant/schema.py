import datetime

from pydantic import BaseModel, ConfigDict


class OpenAIAssistantModelDTO(BaseModel):
    """
    DTO for openai assistant models.

    It returned when accessing openai assistant models from the API.
    """

    openai_assistant_id: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class OpenAIAssistantModelInputDTO(BaseModel):
    """DTO for creating new openai assistant model."""

    openai_assistant_id: str
