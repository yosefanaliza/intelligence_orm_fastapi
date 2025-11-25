"""
FastAPI Server Entry Point - HTTP Server for Intelligence Reporting System

This server sits between the terminal client and the database,
providing a RESTful API for all intelligence operations.

Architecture:
Terminal Client -> HTTP API (this server) -> Services -> DAL -> Database
"""
import uvicorn
from app.main import app
from config import settings


if __name__ == "__main__":
    print("=" * 60)
    print(f"{settings.PROJECT_NAME} API Server")
    print("=" * 60)
    print(f"\nStarting server on http://{settings.HOST}:{settings.PORT}")
    print(f"API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"API v1 Endpoint: http://{settings.HOST}:{settings.PORT}{settings.API_V1_PREFIX}")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="info"
    )
