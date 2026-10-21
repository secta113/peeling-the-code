"""請求額とキャンペーンのルール。"""

from dataclasses import dataclass
from datetime import date

from billing.domain.order import Order


@dataclass(frozen=True)
class Campaign:
    end: date
    rate: float = 0.95

    def applies(self, today: date) -> bool:
        return today <= self.end


CAMPAIGN = Campaign(end=date(2026, 11, 30))  # 年末キャンペーン


def calc_invoice(order: Order) -> int:
    """第1回で分割した計算（デモ用に簡略化）。"""
    return sum(item.price * item.qty for item in order.items)
