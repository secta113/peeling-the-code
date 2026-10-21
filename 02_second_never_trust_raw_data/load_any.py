"""18ページ: json は Unknown（暗黙の Any）。Pyrefly は黙る。"""
import json
import pathlib
from typing import reveal_type

order = json.loads(pathlib.Path("order.json").read_text(encoding="utf-8"))
item = order["items"][0]

reveal_type(item["price"])
amount = item["price"] * item["qty"]
