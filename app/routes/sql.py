"""
SQL endpoint routes
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, text
from db.database import get_engine

router = APIRouter()


class SQLQuery(BaseModel):
    """Schema for SQL query"""
    query: str


@router.post("/execute")
def execute_sql_endpoint(sql_data: SQLQuery):
    """
    Execute a raw SQL query
    
    **WARNING**: This endpoint is for development/admin use only.
    It can execute any SQL query, including destructive operations.
    
    - **query**: SQL query to execute
    """
    try:
        engine = get_engine()
        with Session(engine) as session:
            result = session.execute(text(sql_data.query))
            
            # Try to fetch results (for SELECT queries)
            try:
                rows = result.fetchall()
                # Convert rows to list of dicts
                if rows:
                    columns = result.keys()
                    results = [dict(zip(columns, row)) for row in rows]
                    return {
                        "success": True,
                        "row_count": len(results),
                        "results": results
                    }
                else:
                    return {
                        "success": True,
                        "message": "Query executed successfully (no results)"
                    }
            except Exception:
                # For non-SELECT queries (INSERT, UPDATE, DELETE, etc.)
                session.commit()
                return {
                    "success": True,
                    "message": "Query executed successfully"
                }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SQL execution failed: {str(e)}"
        )
