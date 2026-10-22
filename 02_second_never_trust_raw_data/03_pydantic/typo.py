"""26ページ: 同じ打ち間違いを、dict とモデルでどう扱うか。
   ①と②を交互にコメントアウトして pyrefly check 03_pydantic/typo.py を走らせる。
"""
import json
import pathlib

from models import Order

raw = json.loads(
    (pathlib.Path(__file__).parent / "order.json").read_text(encoding="utf-8")
)

# ① dict のまま → INFO 0 errors（実行して KeyError が出るまで分からない）
print(raw["items"][0]["prise"])

# ② モデルにした後 → ERROR ... has no attribute `prise` / Did you mean `price`?
# order = Order.model_validate(raw)
# print(order.items[0].prise)
