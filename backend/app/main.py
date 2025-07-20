from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from api.v1.endpoints import auth, onboarding, dashboard, tasks
from core.config import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
import os

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create middleware list
middleware = [
    Middleware(SlowAPIMiddleware),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# Create FastAPI app with middleware
app = FastAPI(
    title=settings.PROJECT_NAME,
    middleware=middleware,
    version="2.2"
)

# Set up rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(onboarding.router, prefix=settings.API_V1_STR, tags=["onboarding"])
app.include_router(dashboard.router, prefix=settings.API_V1_STR, tags=["dashboard"])
app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Real Estate CRM API", "version": "2.2"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "RECT API"}

