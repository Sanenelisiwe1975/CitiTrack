"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from .config import settings
from .db import init_db
from .api import reports, dashboard, blockchain, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 CitiTrack API starting...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    
    # Initialize database
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
    
    yield
    
    # Shutdown
    print("👋 CitiTrack API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="CitiTrack API",
    description="API for CitiTrack - Civic Issue Tracking Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(reports.router)
app.include_router(dashboard.router)
app.include_router(blockchain.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CitiTrack API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    from .services import blockchain_service
    
    return {
        "status": "healthy",
        "database": "connected",
        "blockchain": "connected" if blockchain_service.is_connected() else "disconnected",
        "services": {
            "ai": "configured" if settings.OPENAI_API_KEY else "not configured",
            "sms": "configured" if settings.AT_API_KEY else "not configured",
            "storage": "configured" if settings.AWS_ACCESS_KEY_ID else "not configured"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    print(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.ENVIRONMENT == "development"
    )