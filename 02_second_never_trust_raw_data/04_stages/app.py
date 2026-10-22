"""27ページ: 門を通した後は、pydantic は見ていない。

   > python -m 04_stages.app         → 不正なデータが素通りする
   > pyrefly check 04_stages/app.py  → 静的側が捕まえる
"""
import json
import pathlib

from models import Order

raw = json.loads(
    (pathlib.Path(__file__).parent / "order.json").read_text(encoding="utf-8")
)
o = Order.model_validate(raw)          # ここは検証される

o.items.append({"category": "food", "price": "たぶん300", "qty": 0})

print(o.items[-1])                     # Item にすらならず dict のまま
print(type(o.items[-1]).__name__)

# 既定では、再代入も検証されません
o.items = [{"category": "x", "price": -1, "qty": 0}]
print(o.items)

# model_dump すると警告は出ますが、処理は止まりません
print(o.model_dump())
