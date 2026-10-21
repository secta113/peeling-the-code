"""第3回 デモ用：患者のコード（治療前）。

請求額を計算して、DB に保存して、メールで送る。
関数の中で、時計・DB・メール API を自分で取りに行っている。
"""

import sqlite3
from datetime import date

import requests
from pydantic import BaseModel, Field

# 本番のメール API のつもり。デモでは scripts/fake_mail_server.py が受ける。
MAIL_API_URL = "http://localhost:8025/send"


class Item(BaseModel):
    category: str
    price: int = Field(ge=0)
    qty: int = Field(ge=1)


class OrderIn(BaseModel):
    order_id: str
    email: str
    items: tuple[Item, ...]


def calc_invoice(order: OrderIn) -> int:
    """第1回で分割した計算（デモ用に簡略化）。"""
    return sum(item.price * item.qty for item in order.items)


def issue_invoice(order: OrderIn) -> int:
    total = calc_invoice(order)
    if date.today() <= date(2026, 11, 30):  # 年末キャンペーン
        total = int(total * 0.95)
    conn = sqlite3.connect("C:/billing/prod.db")
    conn.execute("INSERT INTO invoices VALUES (?, ?)", (order.order_id, total))
    conn.commit()
    requests.post(
        MAIL_API_URL,
        json={"to": order.email, "body": f"ご請求額 {total}円"},
        timeout=5,
    )
    return total
