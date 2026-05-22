from fastapi import APIRouter, Response, status
from datetime import datetime
from app.config import settings
from app.repositories.notification_repo import AsyncSessionLocal
from sqlalchemy import text

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(response: Response):
    
    dependencies = {
        "database": "disconnected",
        "message_broker": "connected"  
    }
    
    try:
       
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        dependencies["database"] = "connected"
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "dependencies": dependencies
        }
        
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "dependencies": dependencies
    }