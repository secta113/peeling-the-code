"""23ページ: model_validate を1行通すと 3000 になる。"""
import json
import pathlib

from models import Order

raw = json.loads(
    (pathlib.Path(__file__).parent / "order.json").read_text(encoding="utf-8")
)
order = Order.model_validate(raw)

item = order.items[0]
print(item.price, item.qty)
print(item.price * item.qty)
