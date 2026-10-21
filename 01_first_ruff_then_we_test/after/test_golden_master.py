"""ゴールデンマスターテスト: 今の振る舞いを「正解」として固定する"""
import itertools
import json
import pathlib

import pytest

from billing import calc_invoice

GOLDEN = pathlib.Path(__file__).parent / "golden_master.json"


def all_cases():
    """入力の組み合わせを機械的に作る（人間が考えない）"""
    item_sets = [
        [{"category": "book", "price": 1500, "qty": 2}],
        [{"category": "food", "price": 300, "qty": 12}],
        [
            {"category": "book", "price": 4000, "qty": 3},
            {"category": "other", "price": 800, "qty": 1},
        ],
    ]
    ranks = ["gold", "silver", "bronze", "none"]
    coupons = ["SPRING", "NEWYEAR", None]
    ship_tos = ["remote", "island", "normal"]
    pays = ["cod", "bank", "card"]
    return list(itertools.product(item_sets, ranks, coupons, ship_tos, pays))


def make_golden():
    """現行コードの出力を丸ごと記録する（リファクタリング前に1回だけ実行）"""
    return [
        {
            "input": [items, rank, coupon, ship, pay],
            "output": calc_invoice(items, rank, coupon, ship, pay),
        }
        for items, rank, coupon, ship, pay in all_cases()
    ]


@pytest.mark.skipif(GOLDEN.exists(), reason="ゴールデンマスターは作成済み")
def test_create_golden_master():
    GOLDEN.write_text(
        json.dumps(make_golden(), ensure_ascii=False, indent=2), encoding="utf-8"
    )


def test_behavior_is_unchanged():
    """リファクタリングのたびに実行する。1円でも変わったら落ちる"""
    expected = json.loads(GOLDEN.read_text(encoding="utf-8"))
    actual = make_golden()
    assert actual == expected
