# app/db/repositories/property.py

from sqlalchemy.ext.asyncio import AsyncSession
from db.models.property import Property  # Adjust the import if your Property model path differs

class PropertyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_property_by_id(self, property_id):
        result = await self.session.get(Property, property_id)
        return result

    # Add other CRUD methods as needed
