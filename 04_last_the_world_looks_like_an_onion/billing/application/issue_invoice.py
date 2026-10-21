"""請求書を発行する流れ。"""

from datetime import date

from billing.application.ports import InvoiceRepository, Mailer
from billing.domain.order import Order
from billing.domain.pricing import CAMPAIGN, calc_invoice


def issue_invoice(
    order: Order,
    today: date,
    invoices: InvoiceRepository,
    mailer: Mailer,
) -> int:
    total = calc_invoice(order)
    if CAMPAIGN.applies(today):
        total = int(total * CAMPAIGN.rate)
    invoices.save(order.order_id, total)
    mailer.send(order.email, f"ご請求額 {total}円")
    return total
