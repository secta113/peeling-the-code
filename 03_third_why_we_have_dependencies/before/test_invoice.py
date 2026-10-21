"""第3回 デモ①：ふつうにテストを書くと、こうなる。"""

from billing import OrderIn, issue_invoice

SAMPLE = {
    "order_id": "A-1042",
    "email": "taro@example.com",
    "items": [{"category": "book", "price": 1500, "qty": 2}],
}


def test_issue_invoice() -> None:
    order = OrderIn.model_validate(SAMPLE)
    assert issue_invoice(order) == 2850
