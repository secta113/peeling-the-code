"""外から届く注文の形（第2回の pydantic の門）。"""

from pydantic import BaseModel, Field


class Item(BaseModel):
    category: str
    price: int = Field(ge=0)
    qty: int = Field(ge=1)


class OrderIn(BaseModel):
    order_id: str
    email: str
    items: tuple[Item, ...]
