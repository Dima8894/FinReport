"""
FinReportAI Backend Application

FastAPI entry point with CORS, middleware, and API routing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1 import router as api_v1_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Автоматизированная финансовая отчетность для малого и среднего бизнеса",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=settings.DEBUG
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/health")
async def health_check():
    """
    Health check для Railway и monitoring систем
    """
    # TODO: Add actual DB and Redis health checks
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected",
        "redis": "connected"
    }


# Include API v1 router
app.include_router(
    api_v1_router,
    prefix=settings.API_V1_PREFIX
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler для непойманных ошибок
    """
    # TODO: Add proper logging with structlog
    import traceback
    
    error_detail = str(exc)
    if settings.DEBUG:
        error_detail = traceback.format_exc()
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": error_detail if settings.DEBUG else "Something went wrong"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Only for development
        log_level="info"
    )
