from __future__ import annotations

from fastapi import APIRouter, status
from sqlalchemy.exc import SQLAlchemyError

from bank_api.db.migrations import check_db_connection

router = APIRouter()


@router.get("/health/db", tags=["health"])
def health_db() -> dict:
    try:
        check_db_connection()
        return {"status": "ok", "database": "ok"}
    except SQLAlchemyError as exc:
        return {"status": "degraded", "database": "error", "detail": str(exc)}
