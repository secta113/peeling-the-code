"""24ページ: 壊れたデータを食わせる。3件まとめて報告される。"""
import json
import pathlib

from pydantic import ValidationError

from models import Order

raw = json.loads(pathlib.Path("order_broken.json").read_text(encoding="utf-8"))
try:
    Order.model_validate(raw)
except ValidationError as e:
    print(e)
