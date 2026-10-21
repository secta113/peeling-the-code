"""第3回 デモ（4章）：関数の奥で os.environ を読むと、途中で落ちる。

使い方（PowerShell）:
  $env:DB_PATH = "env_demo.db"
  Remove-Item Env:MAIL_API_URL -ErrorAction SilentlyContinue
  python env_style.py
"""

import os
import sqlite3

import requests

from billing import OrderIn, calc_invoice

SAMPLE = {
    "order_id": "A-1042",
    "email": "taro@example.com",
    "items": [{"category": "book", "price": 1500, "qty": 2}],
}


def issue_invoice(order: OrderIn) -> int:
    total = int(calc_invoice(order) * 0.95)
    print(f"請求額を計算しました: {total}")

    db_path = os.environ["DB_PATH"]  # 無ければ KeyError
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS invoices (order_id TEXT, total INTEGER)")
        conn.execute("INSERT INTO invoices VALUES (?, ?)", (order.order_id, total))
    print(f"DB に保存しました: {order.order_id}")

    mail_url = os.environ["MAIL_API_URL"]  # ← ここで落ちる
    retry = int(os.environ.get("RETRY", "3"))  # int() で囲む
    for _ in range(retry):
        requests.post(mail_url, json={"to": order.email}, timeout=5)
        break
    return total


if __name__ == "__main__":
    issue_invoice(OrderIn.model_validate(SAMPLE))
