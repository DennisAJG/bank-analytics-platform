from __future__ import annotations

import random
import uuid
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import delete, select

from bank_api.db.models import Account, AccountTransaction, CardInvoice, Customer
from bank_api.db.session import get_sessionmaker


def _now() -> datetime:
    return datetime.now(UTC)


def seed(reset: bool = False) -> None:
    SessionLocal = get_sessionmaker()

    with SessionLocal() as session:
        if reset:
            # ordem respeita FKs
            session.execute(delete(AccountTransaction))
            session.execute(delete(CardInvoice))
            session.execute(delete(Account))
            session.execute(delete(Customer))
            session.commit()

        # evita duplicar seed
        existing = session.execute(select(Customer).limit(1)).scalar_one_or_none()
        if existing:
            return

        customers: list[Customer] = []
        for i in range(1, 21):
            c = Customer(
                external_id=f"CUST-{1000+i}",
                full_name=f"Cliente {i} Exemplo",
                email=f"cliente{i}@example.com",
                status="active",
            )
            customers.append(c)
            session.add(c)

        session.flush()

        # contas
        accounts: list[Account] = []
        for c in customers:
            acc = Account(
                customer_id=c.id,
                account_number=f"000{i:04d}-{c.id:02d}",
                status="open",
                balance=Decimal(str(random.randint(100, 20000))) / Decimal("1.0"),
            )
            accounts.append(acc)
            session.add(acc)

        session.flush()

        now = _now()

        # faturas (algumas overdue)
        for _idx, c in enumerate(customers, start=1):
            due = now - timedelta(days=random.choice([5, 10, 35, -10]))  # algumas no futuro
            status = "unpaid"
            paid_at = None
            if due < now and random.random() < 0.55:
                status = "overdue"
            elif due < now and random.random() < 0.30:
                status = "paid"
                paid_at = due - timedelta(days=1)

            inv = CardInvoice(
                customer_id=c.id,
                invoice_ref=f"INV-{uuid.uuid4().hex[:12]}",
                due_date=due,
                paid_at=paid_at,
                amount=Decimal(str(random.randint(200, 8000))) / Decimal("1.0"),
                status=status,
            )
            session.add(inv)

        # transações (para simular "movimentação")
        # vamos marcar alguns clientes com muitas transações nas últimas 24h
        hot_customer_ids = set(random.sample([c.id for c in customers], k=5))

        for c in customers:
            tx_count = 60 if c.id in hot_customer_ids else random.randint(3, 20)
            for _ in range(tx_count):
                occurred = now - timedelta(
                    hours=random.randint(0, 72), minutes=random.randint(0, 59)
                )
                tx = AccountTransaction(
                    customer_id=c.id,
                    tx_ref=f"TX-{uuid.uuid4().hex[:14]}",
                    occurred_at=occurred,
                    tx_type=random.choice(["debit", "credit", "pix", "transfer"]),
                    amount=Decimal(str(random.randint(5, 2500))) / Decimal("1.0"),
                    description="seed transaction",
                )
                session.add(tx)

        session.commit()
