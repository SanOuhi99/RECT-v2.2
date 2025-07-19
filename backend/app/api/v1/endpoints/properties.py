from fastapi import APIRouter, Depends, HTTPException
from app.db.repositories.property import PropertyRepository
from app.schemas.property import PropertyCreate, PropertyInDB

router = APIRouter()

@router.post("/", response_model=PropertyInDB)
async def create_property(
    property: PropertyCreate,
    repo: PropertyRepository = Depends(PropertyRepository)
):
    return await repo.create_property(property)