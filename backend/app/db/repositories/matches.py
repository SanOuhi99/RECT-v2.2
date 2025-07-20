# app/db/repositories/matches.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import uuid

from db.models.match import Match  # assuming you have this model
from db.schemas.match import MatchCreate, MatchUpdate  # your Pydantic schemas


class MatchRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_match(self, match_id: uuid.UUID) -> Match | None:
        query = select(Match).where(Match.id == match_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_matches_by_user(self, user_id: uuid.UUID) -> List[Match]:
        query = select(Match).where(Match.user_id == user_id).order_by(Match.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_match(self, match_in: MatchCreate) -> Match:
        db_match = Match(**match_in.dict())
        self.session.add(db_match)
        await self.session.commit()
        await self.session.refresh(db_match)
        return db_match

    async def update_match(self, db_match: Match, match_in: MatchUpdate) -> Match:
        update_data = match_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_match, field, value)
        self.session.add(db_match)
        await self.session.commit()
        await self.session.refresh(db_match)
        return db_match

    async def delete_match(self, match_id: uuid.UUID) -> None:
        query = select(Match).where(Match.id == match_id)
        result = await self.session.execute(query)
        db_match = result.scalars().first()
        if db_match:
            await self.session.delete(db_match)
            await self.session.commit()
