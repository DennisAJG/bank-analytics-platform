from __future__ import annotations
from fastapi import APIRouter
from bank_api.observability.metrics import render_prometheus 

router = APIRouter()

@router.get("/metrics", include_in_schema=False)
def metrics():
    return render_prometheus()