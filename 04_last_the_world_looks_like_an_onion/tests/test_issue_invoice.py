"""application のテスト。偽物を渡す（第3回と同じ）。"""

from datetime import date

import pytest

from billing.application.issue_invoice import issue_invoice
from billing.domain.order import Item, Order

ORDER = Order("A-1042", "taro@example.com", (Item("book", 1500, 2),))


class FakeInvoices:
    def __init__(self) -> None:
        self.saved: list[tuple[str, int]] = []

    def save(self, order_id: str, total: int) -> None:
        self.saved.append((order_id, total))


class FakeMailer:
    def __init__(self) -> None:
        self.sent: list[str] = []

    def send(self, to: str, body: str) -> None:
        self.sent.append(to)


def test_campaign_discount_is_applied() -> None:
    invoices, mailer = FakeInvoices(), FakeMailer()
    total = issue_invoice(ORDER, date(2026, 11, 30), invoices, mailer)
    assert total == 2850
    assert invoices.saved == [("A-1042", 2850)]
    assert mailer.sent == ["taro@example.com"]


@pytest.mark.parametrize(
    ("today", "expected"),
    [
        (date(2026, 11, 30), 2850),  # 境界: 最終日は割引
        (date(2026, 12, 1), 3000),  # 翌日は定価
    ],
)
def test_campaign_boundary(today: date, expected: int) -> None:
    assert issue_invoice(ORDER, today, FakeInvoices(), FakeMailer()) == expected
