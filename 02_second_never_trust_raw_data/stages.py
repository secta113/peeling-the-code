"""28ページ: 段階の数だけモデルを作る。

   > python stages.py         → 正しい順番なら通る
   > pyrefly check stages.py  → 段階を飛ばすと止まる
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Rank = Literal["gold", "silver", "bronze", "none"]
RANK_DISCOUNT = {"gold": 0.90, "silver": 0.95, "bronze": 0.98, "none": 1.0}


class Item(BaseModel):
    model_config = ConfigDict(frozen=True)   # 属性への代入を止める
    category: str
    price: int = Field(ge=0)
    qty: int = Field(ge=1)


class OrderIn(BaseModel):
    """外から届いた状態。金額はまだ確定していない。"""
    order_id: str
    member_rank: Rank
    items: tuple[Item, ...]                  # tuple なので append できない


class OrderPriced(BaseModel):
    """金額が確定した状態。"""
    order_id: str
    items: tuple[Item, ...]
    subtotal: int = Field(ge=0)
    total: int = Field(ge=0)


def price_order(o: OrderIn) -> OrderPriced:
    """未確定を受け取って、確定を返す。関数の形が段階そのものになる。"""
    sub = sum(i.price * i.qty for i in o.items)
    return OrderPriced(order_id=o.order_id, items=o.items,
                       subtotal=sub, total=int(sub * RANK_DISCOUNT[o.member_rank]))


def issue_invoice(o: OrderPriced) -> str:
    return f"{o.order_id}: {o.total} 円"


raw = {"order_id": "A-1", "member_rank": "gold",
       "items": [{"category": "book", "price": 1500, "qty": 2}]}

incoming = OrderIn.model_validate(raw)
priced = price_order(incoming)
print(issue_invoice(priced))

# append しようとしても、メソッド自体が存在しない
try:
    incoming.items.append(Item(category="food", price=300, qty=1))
except AttributeError as e:
    print("append できない:", e)

# 段階を飛ばす ― Pyrefly は実行前に止める。実行すると本番で落ちる
try:
    print(issue_invoice(incoming))
except AttributeError as e:
    print("段階を飛ばすと実行時に落ちる:", e)
