from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gainzai_assignment.db.dependencies import get_db_session
from gainzai_assignment.db.models.openai_assistants import OpenAIAssistantDbModel


class OpenAIAssistantDAO:
    """Class for accessing openai_assistants table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_openai_assistant_model(self, openai_assistant_id: str) -> None:
        """
        Add single openai assistant to session.

        :param openai_assistant_id: open ai generated assistant_id
        """
        self.session.add(
            OpenAIAssistantDbModel(openai_assistant_id=openai_assistant_id)
        )

    async def get_all_openai_assistants(
        self,
        limit: int,
        offset: int,
    ) -> List[OpenAIAssistantDbModel]:
        """
        Get all openai assistants with limit/offset pagination.

        :param limit: limit of assistants.
        :param offset: offset of assistants.
        :return: stream of assistants.
        """
        raw_assistants = await self.session.execute(
            select(OpenAIAssistantDbModel).limit(limit).offset(offset),
        )

        return list(raw_assistants.scalars().fetchall())

    async def filter(self, openai_assistant_id: str) -> List[OpenAIAssistantDbModel]:
        """
        Get specific OpenAI Assistant model.

        :param openai_assistant_id: open ai generated assistant_id
        :return: openai assistant models.
        """
        query = select(OpenAIAssistantDbModel)
        if openai_assistant_id:
            query = query.where(
                OpenAIAssistantDbModel.openai_assistant_id == openai_assistant_id,
            )
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
