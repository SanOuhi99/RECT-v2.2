from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.schemas.user import UserCreate, UserInDB

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, *, email: str, hashed_password: str, full_name: str, 
                        company_id: int, kvcore_token: str) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            company_id=company_id,
            kvcore_token=kvcore_token,
            is_active=True
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user_last_login(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(user)
        return user