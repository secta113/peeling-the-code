"""第3回 デモ②：形を間違えた偽物を渡すと、Pyrefly が実行前に止める。

使い方: pyrefly check demos/wrong_fake.py
"""

from datetime import date

from billing.invoice import issue_invoice
from billing.models import OrderIn


class FakeInvoices:
    def save(self, order_id: str, total: int) -> None:
        pass


class FakeMailer:
    def send(self, to: str) -> None:  # body を書き忘れた
        pass


order = OrderIn(order_id="A-1042", email="taro@example.com", items=())
issue_invoice(order, date(2026, 11, 30), FakeInvoices(), FakeMailer())
