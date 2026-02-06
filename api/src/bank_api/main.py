from __future__ import annotations

from fastapi import FastAPI

from bank_api.api.routes.health import router as health_router
from bank_api.api.routes.health_db import router as health_db_router
from bank_api.api.routes.metrics import router as metrics_router
from bank_api.api.routes.reports import router as reports_router
from bank_api.logging import get_logger
from bank_api.observability.metrics import metrics_middleware
from bank_api.settings import settings

log = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    app.middleware("http")(metrics_middleware)
    app.include_router(health_router)
    app.include_router(health_db_router)
    app.include_router(metrics_router)
    app.include_router(reports_router)

    log.info("app_started", env=settings.environment)
    return app


app = create_app()
