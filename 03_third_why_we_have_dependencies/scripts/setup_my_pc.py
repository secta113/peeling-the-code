"""デモ用：「自分の PC」を再現する。C:/billing/prod.db を作り、invoices テーブルを用意する。

before/ の患者のコードが前提にしている環境です。
使い方: python scripts/setup_my_pc.py
"""

import sqlite3
from pathlib import Path

DB = Path("C:/billing/prod.db")

if __name__ == "__main__":
    DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS invoices (order_id TEXT, total INTEGER)"
        )
    print(f"作成しました: {DB.resolve()}")
