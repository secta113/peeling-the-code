"""17ページ: 型注釈は実行時には何もしない。
   > mypy check.py    → error
   > python check.py  → 'abcabc'
"""


def price_of(x: int) -> int:
    return x * 2


print(repr(price_of("abc")))
