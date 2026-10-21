"""19ページ: 実行して '15001500' を見せる用（reveal_type なし）。"""
import json
import pathlib

order = json.loads(pathlib.Path("order.json").read_text(encoding="utf-8"))
item = order["items"][0]
print(repr(item["price"] * item["qty"]))
