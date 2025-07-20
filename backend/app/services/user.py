from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserInDB, UserUpdate
from db.repositories.user import UserRepository

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def get_user_by_id(self, user_id: int) -> Optional[UserInDB]:
        user = await self.user_repo.get_user_by_id(user_id)
        if user:
            return UserInDB.from_orm(user)
        return None

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserInDB]:
        user = await self.user_repo.update_user(user_id, user_data)
        if user:
            return UserInDB.from_orm(user)
        return None

    async def update_kvcore_token(self, user_id: int, token: str) -> Optional[UserInDB]:
        user = await self.user_repo.update_kvcore_token(user_id, token)
        if user:
            return UserInDB.from_orm(user)
        return None
