from __future__ import annotations
from fastapi import FastAPI

from bank_api.api.routes.health import router as health_router
from bank_api.api.routes.metrics import router as metrics_router
from bank_api.logging import configure_logging, get_logger
from bank_api.observability.metrics import metrics_middleware
from bank_api.settings import settgins

log = get_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settgins.app_name,
        version="0.1.0",
    )
    
    app.middleware("http")(metrics_middleware)
    app.include_router(health_router)
    app.include_router(metrics_router)  
    
    log.info("app_started", env=settgins.enviroment)   
    return app

app = create_app()