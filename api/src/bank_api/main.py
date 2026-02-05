from __future__ import annotations
from fastapi import FastAPI
from bank_api.settings import settgins
from bank_api.api.routes.health import router as health_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settgins.app_name,
        version="0.1.0",
    )
    
    app.include_router(health_router)
    
    return app

app = create_app()