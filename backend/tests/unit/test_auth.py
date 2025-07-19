# backend/tests/unit/test_auth.py
import pytest
from fastapi import status
from app.db.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.auth import AuthService

@pytest.mark.asyncio
async def test_user_registration(db_session):
    user_repo = UserRepository(db_session)
    auth_service = AuthService(user_repo)
    
    new_user = UserCreate(
        email="test@example.com",
        password="securepassword",
        full_name="Test User"
    )
    
    user = await auth_service.register_user(new_user)
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"