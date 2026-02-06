from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from bank_api.db.models import CardInvoice, AccountTransaction, Customer


def get_unpaid_invoices(
    session: Session,
    as_of: datetime,
):
    stmt = (
        select(
            Customer.id,
            Customer.full_name,
            Customer.email,
            CardInvoice.invoice_ref,
            CardInvoice.due_date,
            CardInvoice.amount,
            CardInvoice.status,
        )
        .join(CardInvoice, CardInvoice.customer_id == Customer.id)
        .where(
            CardInvoice.status.in_(["unpaid", "overdue"]),
            CardInvoice.due_date <= as_of,
        )
        .order_by(CardInvoice.due_date.asc())
    )

    return session.execute(stmt).all()


def get_high_account_activity(
    session: Session,
    since: datetime,
    min_transactions: int,
):
    stmt = (
        select(
            Customer.id,
            Customer.full_name,
            Customer.email,
            func.count(AccountTransaction.id).label("tx_count"),
            func.sum(AccountTransaction.amount).label("total_amount"),
        )
        .join(AccountTransaction, AccountTransaction.customer_id == Customer.id)
        .where(AccountTransaction.occurred_at >= since)
        .group_by(Customer.id)
        .having(func.count(AccountTransaction.id) >= min_transactions)
        .order_by(func.count(AccountTransaction.id).desc())
    )

    return session.execute(stmt).all()
