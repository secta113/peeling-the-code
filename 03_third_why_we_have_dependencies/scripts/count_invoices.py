"""デモ用：テストを走らせたあと、「本番 DB」に請求書が何件増えたかを見る。

使い方: python scripts/count_invoices.py
"""

import sqlite3
from pathlib import Path

DB = Path("C:/billing/prod.db")

if __name__ == "__main__":
    with sqlite3.connect(DB) as conn:
        rows = conn.execute("SELECT order_id, total FROM invoices").fetchall()
    print(f"本番 DB の請求書: {len(rows)} 件")
    for order_id, total in rows:
        print(f"  {order_id}: {total}円")
