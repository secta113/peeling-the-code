"""12ページ: 型注釈がないと、型チェッカは何も言わない。
   > pyrefly check untyped.py  →  INFO 0 errors
"""

COUPONS = {"SPRING": 0.95, "NEWYEAR": 0.90}


def find_coupon(code):
    return COUPONS.get(code)


def apply_coupon(amount, code):
    rate = find_coupon(code)
    return amount * rate       # None なら落ちる。でも指摘されない
