"""コンポジションルート。全部の層を import してよい、唯一の場所。

使い方: python -m billing.main   （.env が必要。.env.example をコピーする）
"""

import json
from datetime import date
from pathlib import Path

from billing.application.issue_invoice import issue_invoice
from billing.infrastructure.http_mailer import HttpMailer
from billing.infrastructure.order_in import OrderIn
from billing.infrastructure.settings import Settings
from billing.infrastructure.sqlite_repo import SqliteInvoiceRepository


def load_order() -> OrderIn:
    raw = json.loads(Path("orders/sample.json").read_text(encoding="utf-8"))
    return OrderIn.model_validate(raw)


def main() -> None:
    settings = Settings()
    invoices = SqliteInvoiceRepository(settings.db_path)
    mailer = HttpMailer(str(settings.mail_api_url), settings.retry)
    total = issue_invoice(load_order().to_domain(), date.today(), invoices, mailer)
    print(f"請求書を発行しました: {total}円")


if __name__ == "__main__":
    main()
