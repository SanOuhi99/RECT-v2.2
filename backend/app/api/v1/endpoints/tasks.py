from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from app.schemas.task import TaskStatus
from app.services.matching import MatchingService
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

@router.post("/matching/start", response_model=TaskStatus)
async def start_matching_task(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Start background property matching task"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    matching_service = MatchingService(db)
    try:
        task_id = await matching_service.start_matching_for_user(current_user.id)
        return {"task_id": task_id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matching/status/{task_id}", response_model=TaskStatus)
async def get_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Check status of background task"""
    matching_service = MatchingService(db)
    return await matching_service.get_task_status(task_id)