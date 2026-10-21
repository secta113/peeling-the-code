"""講習デモ用: リファクタリング前の「長い関数」"""


def calc_invoice(items, member_rank, coupon, ship_to, pay_method):
    total = 0
    for it in items:
        price = it["price"] * it["qty"]
        if it["category"] == "book":
            price = price * 0.95
        elif it["category"] == "food":
            price = price * 0.98
        total += price

    if member_rank == "gold":
        total = total * 0.90
    elif member_rank == "silver":
        total = total * 0.95
    elif member_rank == "bronze":
        total = total * 0.98

    if coupon == "SPRING":
        total = total - 500
    elif coupon == "NEWYEAR":
        total = total - 1000
    if total < 0:
        total = 0

    if ship_to == "remote":
        ship = 1200
    elif ship_to == "island":
        ship = 2000
    else:
        ship = 600
    if total >= 10000:
        ship = 0
    total = total + ship

    if pay_method == "cod":
        total = total + 330
    elif pay_method == "bank":
        total = total + 220

    tax = 0
    for it in items:
        if it["category"] == "food":
            tax += it["price"] * it["qty"] * 0.08
        else:
            tax += it["price"] * it["qty"] * 0.10
    total = total + tax

    return int(total)
