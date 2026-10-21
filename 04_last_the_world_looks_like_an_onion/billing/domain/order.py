"""業務の形。pydantic を知らない。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    category: str
    price: int
    qty: int


@dataclass(frozen=True)
class Order:
    order_id: str
    email: str
    items: tuple[Item, ...]
