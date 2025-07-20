from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List

from db.schemas.match import MatchResponse
from services.matching import MatchingService
from db.session import get_db
from core.security import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

@router.get("/matches", response_model=List[MatchResponse])
async def get_recent_matches(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get recent matches for the current user"""
    matching_service = MatchingService(db)
    return await matching_service.get_recent_matches(current_user.id)

@router.get("/stats")
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get dashboard statistics"""
    return {
        "total_matches": 42,
        "new_this_week": 5,
        "success_rate": 0.92
    }
