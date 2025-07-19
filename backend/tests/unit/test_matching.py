# backend/tests/unit/test_matching.py
import pytest
from app.services.matching import MatchingService
from app.db.repositories.user import UserRepository
from app.db.repositories.company import CompanyRepository

@pytest.mark.asyncio
async def test_property_matching(db_session, sample_properties):
    user_repo = UserRepository(db_session)
    company_repo = CompanyRepository(db_session)
    matching_service = MatchingService(user_repo, company_repo)
    
    matches = await matching_service.find_matches(sample_properties[0])
    assert isinstance(matches, list)
    assert len(matches) > 0
    assert all('score' in match for match in matches)