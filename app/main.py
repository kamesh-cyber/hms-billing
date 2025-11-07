from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from app.service.database import engine, get_db, Base
from app.utility.seed_data import seed_database
from app.utility.middleware import LoggingMiddleware
from app.routes import bills, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting billing service...")

    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

    # Seed database
    logger.info("Seeding database with initial data...")
    db = next(get_db())
    try:
        seed_database(db)
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Failed to seed database: {str(e)}")
    finally:
        db.close()

    logger.info("Billing service started successfully on port 3002")

    yield

    # Shutdown
    logger.info("Shutting down billing service...")


app = FastAPI(
    title="Billing Service",
    description="HMS Billing Service API",
    version="1.0.0",
    lifespan=lifespan
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health.router)
app.include_router(bills.router)


@app.get("/")
async def root():
    """Root endpoint - Service information"""
    return {
        "service": "Billing Service",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health_live": "/health/live",
            "health_ready": "/health/ready",
            "docs": "/docs"
        }
    }


