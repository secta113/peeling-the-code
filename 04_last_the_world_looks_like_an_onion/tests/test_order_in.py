"""門（OrderIn）を通ると、業務の形（Order）になる。"""

from billing.domain.order import Item, Order
from billing.infrastructure.order_in import OrderIn


def test_order_in_becomes_domain_order() -> None:
    raw = {
        "order_id": "A-1042",
        "email": "taro@example.com",
        "items": [{"category": "book", "price": "1500", "qty": 2}],
    }
    assert OrderIn.model_validate(raw).to_domain() == Order(
        "A-1042", "taro@example.com", (Item("book", 1500, 2),)
    )
