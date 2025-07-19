from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserInDB
from app.services.auth import AuthService
from app.db.session import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

@router.post("/verify-company")
async def verify_company_code(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    """Verify if a company code is valid"""
    auth_service = AuthService(db)
    company = await auth_service.verify_company_code(code)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company code"
        )
    return {"valid": True, "company_name": company.name}

@router.post("/signup", response_model=UserInDB)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new user with company verification"""
    auth_service = AuthService(db)
    try:
        user = await auth_service.create_user(user_data)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )