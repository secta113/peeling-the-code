"""Mailer の本物。Mailer を import も継承もしていない（形で合う）。"""

import requests


class HttpMailer:
    def __init__(self, url: str, retry: int = 3) -> None:
        self._url = url
        self._retry = retry

    def send(self, to: str, body: str) -> None:
        for attempt in range(1, self._retry + 1):
            try:
                requests.post(self._url, json={"to": to, "body": body}, timeout=5)
                return
            except requests.RequestException:
                if attempt == self._retry:
                    raise
