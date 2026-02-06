import os

import httpx
import pytest


@pytest.mark.integration
def test_health_db():
    base_url = os.getenv("INTEGRATION_BASE_URL", "http://localhost:8001")
    r = httpx.get(f"{base_url}/health/db", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
