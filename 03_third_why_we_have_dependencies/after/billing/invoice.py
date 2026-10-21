"""Step 1：隠れた依存を、引数に出した後の業務ロジック。

sqlite3 も requests も import していない。
"""

from datetime import date

from billing.models import OrderIn
from billing.ports import InvoiceRepository, Mailer

CAMPAIGN_END = date(2026, 11, 30)  # 年末キャンペーンの最終日


def calc_invoice(order: OrderIn) -> int:
    """第1回で分割した計算（デモ用に簡略化）。"""
    return sum(item.price * item.qty for item in order.items)


def issue_invoice(
    order: OrderIn,
    today: date,
    invoices: InvoiceRepository,
    mailer: Mailer,
) -> int:
    total = calc_invoice(order)
    if today <= CAMPAIGN_END:
        total = int(total * 0.95)
    invoices.save(order.order_id, total)
    mailer.send(order.email, f"ご請求額 {total}円")
    return total
