"""Step 4：Protocol の形に合わせた、本物の部品。"""

import sqlite3
from pathlib import Path

import requests


class SqliteInvoiceRepository:  # InvoiceRepository の本物
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def save(self, order_id: str, total: int) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS invoices (order_id TEXT, total INTEGER)")
            conn.execute("INSERT INTO invoices VALUES (?, ?)", (order_id, total))


class HttpMailer:  # Mailer の本物
    def __init__(self, url: str, retry: int = 3) -> None:
        self._url = url
        self._retry = retry

    def send(self, to: str, body: str) -> None:
        for attempt in range(1, self._retry + 1):
            try:
                requests.post(self._url, json={"to": to, "body": body}, timeout=5)
                return
            except requests.RequestException:
                if attempt == self._retry:
                    raise
