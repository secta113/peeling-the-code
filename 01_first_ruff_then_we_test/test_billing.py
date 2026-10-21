"""分割したから書けるようになった、小さくて読めるテスト"""
import pytest

from billing import apply_coupon, apply_rank_discount, shipping_fee


def test_gold_rank_gets_10_percent_off():
    assert apply_rank_discount(10000, "gold") == 9000


def test_unknown_rank_is_not_discounted():
    assert apply_rank_discount(10000, "none") == 10000


@pytest.mark.parametrize(
    ("amount", "coupon", "expected"),
    [
        (5000, "SPRING", 4500),
        (5000, "NEWYEAR", 4000),
        (5000, None, 5000),
        (300, "NEWYEAR", 0),  # マイナスにならない
    ],
)
def test_apply_coupon(amount, coupon, expected):
    assert apply_coupon(amount, coupon) == expected


@pytest.mark.parametrize(
    ("amount", "ship_to", "expected"),
    [
        (9999, "normal", 600),
        (10000, "normal", 0),  # 境界: ちょうどで無料になる
        (10001, "normal", 0),
        (5000, "remote", 1200),
        (5000, "island", 2000),
    ],
)
def test_shipping_fee(amount, ship_to, expected):
    assert shipping_fee(amount, ship_to) == expected
