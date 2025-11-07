from fastapi import APIRouter, status
from sqlalchemy import text
from app.service.database import engine
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_probe():
    """
    Liveness probe endpoint.

    Returns 200 if the service is alive and running.
    This endpoint does not require authentication.
    """
    return {
        "status": "alive",
        "service": "billing_service"
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_probe():
    """
    Readiness probe endpoint.

    Returns 200 if the service is ready to accept requests.
    Checks database connectivity.
    This endpoint does not require authentication.
    """
    try:
        # Check database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.debug("Readiness check passed - database connection successful")
        return {
            "status": "ready",
            "service": "billing_service",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return {
            "status": "not_ready",
            "service": "billing_service",
            "database": "disconnected",
            "error": str(e)
        }

