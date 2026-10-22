"""17ページ: 型注釈は実行時には何もしない。
   > pyrefly check 01_types/check.py  → error
   > python -m 01_types.check         → 'abcabc'
"""


def price_of(x: int) -> int:
    return x * 2


print(repr(price_of("abc")))
