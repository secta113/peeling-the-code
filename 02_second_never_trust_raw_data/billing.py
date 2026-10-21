"""第2回デモ。第1回の請求計算コードの一部。"""

COUPONS = {"SPRING": 0.95, "NEWYEAR": 0.90}


def find_coupon(code: str) -> float | None:
    return COUPONS.get(code)


def apply_coupon(amount: float, code: str) -> float:
    rate = find_coupon(code)
    return amount * rate


def shipping_fee(amount: float, ship_to: str) -> int:
    if amount >= 10000:
        return 0
    return 1200 if ship_to == "remote" else 600


def total(amount: float, ship_to: str) -> float:
    return amount + shipping_fee(ship_to, amount)
