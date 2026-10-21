"""Step 2：「何が必要か」だけを Protocol で書く。"""

from typing import Protocol


class InvoiceRepository(Protocol):
    def save(self, order_id: str, total: int) -> None: ...


class Mailer(Protocol):
    def send(self, to: str, body: str) -> None: ...
