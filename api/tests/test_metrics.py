from fastapi.testclient import TestClient

from bank_api.main import app

client = TestClient(app)


def test_metrics_endpoint_exposes_prometheus_text():
    r = client.get("/metrics")
    assert r.status_code == 200
    # formato Prometheus text exposition
    assert "text/plain" in r.headers.get("content-type", "")
    assert "# HELP" in r.text or "# TYPE" in r.text
