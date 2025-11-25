"""
API v1 Router
"""
from fastapi import APIRouter
from app.routes.agents_routes import router as agents_router
from app.routes.terrorists_routes import router as terrorists_router
from app.routes.reports_routes import router as reports_router
from app.routes.sql_routes import router as sql_router

api_router = APIRouter()

api_router.include_router(agents_router, prefix="/agents", tags=["agents"])
api_router.include_router(terrorists_router, prefix="/terrorists", tags=["terrorists"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(sql_router, prefix="/sql", tags=["sql"])
