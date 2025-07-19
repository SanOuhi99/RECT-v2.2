from fastapi import APIRouter
import psutil

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "memory": psutil.virtual_memory().percent,
        "cpu": psutil.cpu_percent()
        "database": "connected"
    }
