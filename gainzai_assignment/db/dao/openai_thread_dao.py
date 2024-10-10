from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gainzai_assignment.db.dependencies import get_db_session
from gainzai_assignment.db.models.openai_threads import OpenAIThreadDbModel


class OpenAIThreadDAO:
    """Class for accessing openai_threads table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_openai_thread_model(self, openai_thread_id: str) -> None:
        """
        Add single openai thread to session.

        :param openai_thread_id: open ai generated thread_id
        """
        self.session.add(OpenAIThreadDbModel(openai_thread_id=openai_thread_id))

    async def get_all_openai_threads(
        self,
        limit: int,
        offset: int,
    ) -> List[OpenAIThreadDbModel]:
        """
        Get all openai threads with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_openai_threads = await self.session.execute(
            select(OpenAIThreadDbModel).limit(limit).offset(offset),
        )

        return list(raw_openai_threads.scalars().fetchall())

    async def filter(self, openai_thread_id: str) -> List[OpenAIThreadDbModel]:
        """
        Get specific OpenAI Thread model.

        :param name: name of dummy instance.
        :return: openai thread models.
        """
        query = select(OpenAIThreadDbModel)
        if openai_thread_id:
            query = query.where(
                OpenAIThreadDbModel.openai_thread_id == openai_thread_id,
            )
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
