from typing import Protocol


class Mailer(Protocol):
    def send(self, to: str, body: str) -> None: ...


def issue_invoice(mailer: Mailer) -> None:
    mailer.send("a@example.com", "hi")


class HttpMailer:  # Mailer を import も継承もしていない
    def send(self, to: str, body: str) -> None:
        print(to, body)


class FakeMailer:
    def send(self, to: str) -> None:
        pass


issue_invoice(HttpMailer())
issue_invoice(FakeMailer())
