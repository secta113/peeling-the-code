"""27ページ: 1行が両側で効く。"""
from pydantic import ValidationError

from models import Order, Rank

RATE = {"gold": 0.90, "silver": 0.95, "bronze": 0.98, "none": 1.0}


def discount_rate(rank: Rank) -> float:
    return RATE[rank]


# mypy が言うこと → Argument 1 has incompatible type "Literal['Gold']"
try:
    print(discount_rate("Gold"))
except KeyError as e:
    print("KeyError:", e, "  ← 実行するまで分からない")

# pydantic が言うこと → Input should be 'gold', 'silver', 'bronze' or 'none'
try:
    Order(order_id="A-1044", member_rank="Gold", items=[], ship_to="normal")
except ValidationError as e:
    print(e)
