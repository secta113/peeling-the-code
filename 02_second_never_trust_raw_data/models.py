"""22ページ: 境界に立てる門。"""
from typing import Literal

from pydantic import BaseModel, Field

Rank = Literal["gold", "silver", "bronze", "none"]


class Item(BaseModel):
    category: str
    price: int = Field(ge=0)
    qty: int = Field(ge=1)


class Order(BaseModel):
    order_id: str
    member_rank: Rank
    items: list[Item]
    ship_to: str
