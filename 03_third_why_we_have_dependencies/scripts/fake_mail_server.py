"""デモ用の「本番メール API」の代わり。localhost:8025 で POST を受けて、届いた内容を表示するだけ。

使い方: python scripts/fake_mail_server.py
止めるとき: Ctrl+C
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        print(f"[メール送信] to={body.get('to')}  body={body.get('body')}", flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format: str, *args: object) -> None:
        return  # アクセスログは出さない


if __name__ == "__main__":
    print(
        "偽メールサーバー起動: http://localhost:8025/send  (Ctrl+C で停止)", flush=True
    )
    ThreadingHTTPServer(("localhost", 8025), Handler).serve_forever()
