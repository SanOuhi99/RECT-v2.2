from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.db.repositories.user import UserRepository
from app.db.repositories.matches import MatchRepository
from app.schemas.match import Match, MatchCreate
from app.tasks.matching import run_matching_task
from celery.result import AsyncResult

class MatchingService:
    def __init__(self, user_repo: UserRepository, match_repo: MatchRepository):
        self.user_repo = user_repo
        self.match_repo = match_repo

    async def start_matching_for_user(self, user_id: int):
        """Start background matching task for a user"""
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Start Celery task
        task = run_matching_task.delay(user_id)
        return task.id

    async def get_task_status(self, task_id: str):
        """Check status of background task"""
        task_result = AsyncResult(task_id)
        return {
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None
        }

    async def get_recent_matches(self, user_id: int, limit: int = 10) -> List[Match]:
        """Get recent matches for a user"""
        return await self.match_repo.get_matches_by_user(user_id, limit)

    async def create_match(self, match_data: MatchCreate) -> Match:
        """Create a new property match record"""
        return await self.match_repo.create_match(match_data)
        # backend/app/services/matching.py
    async def match_properties(self, client_requirements):
        properties = await self.property_repo.get_all()
        
        matches = []
        for property in properties:
            score = self.calculate_match_score(property, client_requirements)
            if score >= self.MIN_MATCH_SCORE:
                matches.append({
                    'property': property,
                    'score': score,
                    'match_reasons': self.get_match_reasons(property, client_requirements)
                })
        
        return sorted(matches, key=lambda x: x['score'], reverse=True)