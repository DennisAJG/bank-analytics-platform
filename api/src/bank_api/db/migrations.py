from __future__ import annotations

from bank_api.db.session import get_engine


def check_db_connection() -> None:
    engine = get_engine()
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1;")
