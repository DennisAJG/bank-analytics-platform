from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from bank_api.db.session import get_sessionmaker
from bank_api.services.report_service import (
    report_account_activity,
    report_unpaid_invoices,
)

router = APIRouter(prefix="/reports", tags=["reports"])


def get_db() -> Session:
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/unpaid-invoices")
def unpaid_invoices(db: Session = Depends(get_db)):
    rows = report_unpaid_invoices(db)

    return [
        {
            "customer_id": r.id,
            "name": r.full_name,
            "email": r.email,
            "invoice_ref": r.invoice_ref,
            "due_date": r.due_date,
            "amount": float(r.amount),
            "status": r.status,
        }
        for r in rows
    ]


@router.get("/account-activity")
def account_activity(
    hours: int = Query(24, ge=1, le=168),
    min_transactions: int = Query(20, ge=1),
    db: Session = Depends(get_db),
):
    rows = report_account_activity(
        session=db,
        hours=hours,
        min_transactions=min_transactions,
    )

    return [
        {
            "customer_id": r.id,
            "name": r.full_name,
            "email": r.email,
            "transaction_count": r.tx_count,
            "total_amount": float(r.total_amount or 0),
        }
        for r in rows
    ]
