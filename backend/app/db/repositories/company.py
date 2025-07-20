from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.company import Company
from db.schemas.company import CompanyCreate, CompanyInDB

class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_company_by_id(self, company_id: int) -> Optional[Company]:
        result = await self.db.execute(
            select(Company).where(Company.id == company_id))
        return result.scalars().first()

    async def get_company_by_code(self, code: str) -> Optional[Company]:
        result = await self.db.execute(
            select(Company).where(Company.code == code))
        return result.scalars().first()

    async def create_company(self, company_data: CompanyCreate) -> Company:
        company = Company(
            name=company_data.name,
            code=company_data.code,
            is_active=True
        )
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company
