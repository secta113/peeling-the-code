"""リファクタリング後: 責務ごとに小さな関数へ分割"""

CATEGORY_DISCOUNT = {"book": 0.95, "food": 0.98}
RANK_DISCOUNT = {"gold": 0.90, "silver": 0.95, "bronze": 0.98}
COUPON_AMOUNT = {"SPRING": 500, "NEWYEAR": 1000}
SHIPPING_FEE = {"remote": 1200, "island": 2000}
PAYMENT_FEE = {"cod": 330, "bank": 220}
TAX_RATE = {"food": 0.08}

DEFAULT_SHIPPING = 600
FREE_SHIPPING_THRESHOLD = 10000
DEFAULT_TAX_RATE = 0.10


def subtotal(items):
    """カテゴリ別の値引きを適用した小計"""
    return sum(
        it["price"] * it["qty"] * CATEGORY_DISCOUNT.get(it["category"], 1.0)
        for it in items
    )


def apply_rank_discount(amount, member_rank):
    return amount * RANK_DISCOUNT.get(member_rank, 1.0)


def apply_coupon(amount, coupon):
    return max(0, amount - COUPON_AMOUNT.get(coupon, 0))


def shipping_fee(amount, ship_to):
    if amount >= FREE_SHIPPING_THRESHOLD:
        return 0
    return SHIPPING_FEE.get(ship_to, DEFAULT_SHIPPING)


def payment_fee(pay_method):
    return PAYMENT_FEE.get(pay_method, 0)


def tax(items):
    """税は値引き前の金額にかかる（現行仕様）"""
    return sum(
        it["price"] * it["qty"] * TAX_RATE.get(it["category"], DEFAULT_TAX_RATE)
        for it in items
    )


def calc_invoice(items, member_rank, coupon, ship_to, pay_method):
    amount = subtotal(items)
    amount = apply_rank_discount(amount, member_rank)
    amount = apply_coupon(amount, coupon)
    amount += shipping_fee(amount, ship_to)
    amount += payment_fee(pay_method)
    amount += tax(items)
    return int(amount)
