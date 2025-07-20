from typing import List
from fastapi import HTTPException, status
from celery.result import AsyncResult

from db.repositories.user import UserRepository
from db.repositories.matches import MatchRepository
from db.repositories.property import PropertyRepository
from db.repositories.client import ClientRepository

from schemas.match import Match, MatchCreate
from tasks.matching import run_matching_task


class MatchingService:
    MIN_MATCH_SCORE = 0.7

    def __init__(
        self,
        user_repo: UserRepository,
        match_repo: MatchRepository,
        property_repo: PropertyRepository,
        client_repo: ClientRepository
    ):
        self.user_repo = user_repo
        self.match_repo = match_repo
        self.property_repo = property_repo
        self.client_repo = client_repo

    async def find_matches(self, client_id: int):
        client = await self.client_repo.get(client_id)
        properties = await self.property_repo.get_all()
        
        matches = []
        for property in properties:
            score = self.calculate_match_score(property, client.requirements)
            if score >= self.MIN_MATCH_SCORE:
                matches.append({
                    'property': property,
                    'score': score,
                    'match_reasons': self.get_match_reasons(property, client.requirements)
                })

        return sorted(matches, key=lambda x: x['score'], reverse=True)[:10]

    async def start_matching_for_user(self, user_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        task = run_matching_task.delay(user_id)
        return task.id

    async def get_task_status(self, task_id: str):
        task_result = AsyncResult(task_id)
        return {
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None
        }

    async def get_recent_matches(self, user_id: int, limit: int = 10) -> List[Match]:
        return await self.match_repo.get_matches_by_user(user_id, limit)

    async def create_match(self, match_data: MatchCreate) -> Match:
        return await self.match_repo.create_match(match_data)

    # Placeholder match logic – to be implemented
    def calculate_match_score(self, property, requirements):
        score = 0.0
        
        # Price match (40% weight)
        price_match = 1 - (abs(property.price - requirements.target_price) / requirements.target_price)
        score += price_match * 0.4
        
        # Location match (30% weight)
        score += 0.3 if property.location == requirements.location else 0
        
        # Features match (30% weight)
        feature_matches = sum(
            1 for feature in requirements.features 
            if feature in property.features
        ) / len(requirements.features)
        score += feature_matches * 0.3
        
        return min(max(score, 0), 1)  # Clamp between 0-1

    def get_match_reasons(self, property, client_requirements) -> List[str]:
        # Implement actual reason extraction logic here
        return ["Example reason"]
