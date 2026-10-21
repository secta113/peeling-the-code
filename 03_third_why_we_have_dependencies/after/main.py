"""組み立てるのは、一番外側だけ（コンポジションルート）。

Settings() を作るのも、date.today() を呼ぶのも、ここだけ。
使い方: python main.py   （.env が必要。.env.example をコピーする）
"""

import json
from datetime import date
from pathlib import Path

from billing.infra import HttpMailer, SqliteInvoiceRepository
from billing.invoice import issue_invoice
from billing.models import OrderIn
from billing.settings import Settings


def load_order() -> OrderIn:
    raw = json.loads(Path("orders/sample.json").read_text(encoding="utf-8"))
    return OrderIn.model_validate(raw)


def main() -> None:
    settings = Settings()  # ← ここが門
    invoices = SqliteInvoiceRepository(settings.db_path)
    mailer = HttpMailer(str(settings.mail_api_url), settings.retry)
    total = issue_invoice(load_order(), date.today(), invoices, mailer)
    print(f"請求書を発行しました: {total}円")


if __name__ == "__main__":
    main()
