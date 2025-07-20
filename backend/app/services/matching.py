from db.repositories.matches import MatchRepository
from db.schemas.match import MatchResponse
from sqlalchemy.ext.asyncio import AsyncSession


class MatchingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.match_repo = MatchRepository(db)

    async def get_recent_matches(self, user_id):
        matches = await self.match_repo.get_matches_by_user(user_id)
        return [MatchResponse.from_orm(m) for m in matches]
