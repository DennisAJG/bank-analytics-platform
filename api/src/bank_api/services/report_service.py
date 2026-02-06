from __future__ import annotations
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from bank_api.repos.reports import (
    get_high_account_activity,
    get_unpaid_invoices,
)

def report_unpaid_invoices(session: Session):
    now = datetime.now(timezone.utc)
    return get_unpaid_invoices(session=session, as_of=now)

def report_account_activity(
    session: Session,
    hours: int = 24,
    min_transactions: int = 20,
):
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    return get_high_account_activity(
        session=session,
        since=since,
        min_transactions=min_transactions,
    )