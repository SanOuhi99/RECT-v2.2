from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.endpoints import auth, onboarding, dashboard, tasks
from app.core.config import settings

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
middleware = [
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=["example.com", "*.example.com"]
    )
]

app = FastAPI(middleware=middleware)
app.state.limiter = limiter
app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(onboarding.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to Real Estate CRM API"}