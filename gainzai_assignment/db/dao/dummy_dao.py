from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gainzai_assignment.db.dependencies import get_db_session
from gainzai_assignment.db.models.dummy_model import DummyDbModel


class DummyDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_dummy_model(self, name: str) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(DummyDbModel(name=name))

    async def get_all_dummies(self, limit: int, offset: int) -> List[DummyDbModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(DummyDbModel).limit(limit).offset(offset),
        )

        return list(raw_dummies.scalars().fetchall())

    async def filter(self, name: Optional[str] = None) -> List[DummyDbModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = select(DummyDbModel)
        if name:
            query = query.where(DummyDbModel.name == name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
