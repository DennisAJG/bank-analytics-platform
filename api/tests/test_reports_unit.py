import bank_api.api.routes.reports as reports_routes

from fastapi.testclient import TestClient
from bank_api.main import app


client = TestClient(app)


def test_unpaid_invoices_unit(monkeypatch):
    def fake_report_unpaid_invoices(_db):
        class Row:
            id = 1
            full_name = "Cliente X"
            email = "x@example.com"
            invoice_ref = "INV-TEST"
            due_date = "2026-01-01T00:00:00+00:00"
            amount = 123.45
            status = "overdue"

        return [Row()]

    # patch no módulo da rota (onde a função foi importada)
    monkeypatch.setattr(reports_routes, "report_unpaid_invoices", fake_report_unpaid_invoices)

    r = client.get("/reports/unpaid-invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert data[0]["invoice_ref"] == "INV-TEST"


def test_account_activity_unit(monkeypatch):
    def fake_report_account_activity(*, session, hours, min_transactions):
        class Row:
            id = 2
            full_name = "Cliente Y"
            email = "y@example.com"
            tx_count = 99
            total_amount = 1000.0

        return [Row()]

    monkeypatch.setattr(reports_routes, "report_account_activity", fake_report_account_activity)

    r = client.get("/reports/account-activity?hours=24&min_transactions=20")
    assert r.status_code == 200
    data = r.json()
    assert data[0]["transaction_count"] == 99
