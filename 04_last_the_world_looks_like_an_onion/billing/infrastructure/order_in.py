"""外から届いた注文の形（門）。門を通ったら、業務の形（Order）に変える。"""

from pydantic import BaseModel, Field

from billing.domain.order import Item, Order


class ItemIn(BaseModel):
    category: str
    price: int = Field(ge=0)
    qty: int = Field(ge=1)

    def to_domain(self) -> Item:
        return Item(self.category, self.price, self.qty)


class OrderIn(BaseModel):
    order_id: str
    email: str
    items: tuple[ItemIn, ...]

    def to_domain(self) -> Order:
        return Order(self.order_id, self.email, tuple(i.to_domain() for i in self.items))
