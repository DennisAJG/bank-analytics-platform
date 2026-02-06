import os

import httpx
import pytest


@pytest.mark.integration
def test_unpaid_invoices_report_returns_list():
    base_url = os.getenv("INTEGRATION_BASE_URL", "http://localhost:8001")
    r = httpx.get(f"{base_url}/reports/unpaid-invoices", timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    # com seed, normalmente vem > 0; mas não vamos “quebrar” se seed mudar
    if data:
        row = data[0]
        assert "customer_id" in row
        assert "invoice_ref" in row
        assert "status" in row


@pytest.mark.integration
def test_account_activity_report_returns_list():
    base_url = os.getenv("INTEGRATION_BASE_URL", "http://localhost:8001")
    r = httpx.get(f"{base_url}/reports/account-activity?hours=24&min_transactions=1", timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        row = data[0]
        assert "transaction_count" in row
