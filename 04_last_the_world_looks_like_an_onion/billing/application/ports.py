"""Protocol は「使う側」が持つ。形を決めるのは業務の側。"""

from typing import Protocol


class InvoiceRepository(Protocol):
    def save(self, order_id: str, total: int) -> None: ...


class Mailer(Protocol):
    def send(self, to: str, body: str) -> None: ...
