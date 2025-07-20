# Fix 2: Update backend/app/main.py

import os
import sys
import logging
from pathlib import Path

# Fix import path issues
current_dir = Path(__file__).parent
backend_dir = current_dir.parent
project_root = backend_dir.parent

# Add paths to sys.path
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

# Import your modules with error handling
try:
    from api.v1.endpoints import auth, onboarding, dashboard, tasks
    from core.config import settings
except ImportError as e:
    logging.error(f"Import error: {e}")
    # Try alternative import paths
    try:
        from app.api.v1.endpoints import auth, onboarding, dashboard, tasks
        from app.core.config import settings
    except ImportError as e2:
        logging.error(f"Alternative import also failed: {e2}")
        raise

# Optional Sentry for error tracking
try:
    if os.getenv("SENTRY_DSN"):
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            integrations=[
                FastApiIntegration(auto_enabling_integrations=False),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=0.1,
            environment=os.getenv("ENVIRONMENT", "production"),
        )
except ImportError:
    logging.warning("Sentry not available, skipping error tracking setup")

# Production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["200/hour"])

# Production CORS settings
allowed_origins = [
    "https://*.railway.app",
    "https://*.up.railway.app",
]

# Add custom domain if available
if os.getenv("CUSTOM_DOMAIN"):
    allowed_origins.append(f"https://{os.getenv('CUSTOM_DOMAIN')}")

# Add frontend URL if available
if os.getenv("FRONTEND_URL"):
    allowed_origins.append(os.getenv("FRONTEND_URL"))

app = FastAPI(
    title=getattr(settings, 'PROJECT_NAME', 'Real Estate CRM API'),
    version="2.2.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None,
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*.railway.app", "*.up.railway.app", "localhost", "127.0.0.1"]
)

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routers with error handling
try:
    api_v1_str = getattr(settings, 'API_V1_STR', '/api/v1')
    app.include_router(auth.router, prefix=f"{api_v1_str}/auth", tags=["auth"])
    app.include_router(onboarding.router, prefix=f"{api_v1_str}/onboarding", tags=["onboarding"])
    app.include_router(dashboard.router, prefix=f"{api_v1_str}/dashboard", tags=["dashboard"])
    app.include_router(tasks.router, prefix=f"{api_v1_str}/tasks", tags=["tasks"])
except Exception as e:
    logger.error(f"Error including routers: {e}")

@app.get("/")
async def root():
    return {"message": "Real Estate CRM API", "version": "2.2.0", "status": "production"}

@app.get("/health")
async def health_check():
    try:
        return {
            "status": "healthy",
            "service": "backend",
            "version": "2.2.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "python_path": sys.path[:3]  # For debugging
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Backend service starting up...")
    logger.info(f"Python path: {sys.path[:3]}")
    logger.info(f"Current working directory: {os.getcwd()}")

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Backend service shutting down...")

# For Railway deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",  # Changed from "app.main:app"
        host="0.0.0.0",
        port=port,
        workers=1,
        loop="uvloop",
        http="httptools"
    )
