# app/db/repositories/client.py

from sqlalchemy.ext.asyncio import AsyncSession
from db.models.client import Client  # Adjust if your model path is different

class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_client_by_id(self, client_id):
        return await self.session.get(Client, client_id)

    async def create_client(self, client_data):
        new_client = Client(**client_data)
        self.session.add(new_client)
        await self.session.commit()
        await self.session.refresh(new_client)
        return new_client

    # Add other CRUD methods as needed
