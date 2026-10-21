"""27ページの補足: validate_assignment を付けても、append は止まらない。"""
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Item(BaseModel):
    category: str
    price: int = Field(ge=0)
    qty: int = Field(ge=1)


class Order(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    order_id: str
    items: list[Item]


o = Order(order_id="A-1", items=[Item(category="book", price=1500, qty=2)])

# ① 再代入は止まる
try:
    o.items = [{"category": "x", "price": -1, "qty": 0}]
except ValidationError as e:
    print("再代入は止まった:", str(e).splitlines()[0])

# ② append は止まらない
o.items.append({"category": "food", "price": "たぶん300", "qty": 0})
print("append は通った:", o.items[-1])
