"""InvoiceRepository の本物。業務の側が決めた形（save）に合わせる。"""

import sqlite3
from pathlib import Path


class SqliteInvoiceRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def save(self, order_id: str, total: int) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS invoices (order_id TEXT, total INTEGER)")
            conn.execute("INSERT INTO invoices VALUES (?, ?)", (order_id, total))
