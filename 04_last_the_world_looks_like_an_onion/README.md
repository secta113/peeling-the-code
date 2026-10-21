# 第4回 デモコード：依存の向きを、機械に守らせる

オニオンアーキテクチャの形に並べた請求計算のコードです。コマンドは PowerShell 前提です。

```
billing/
  domain/          中心。業務ルール。ruff.toml で外側を禁止
  application/     業務の流れと Protocol。ruff.toml で infrastructure を禁止
  infrastructure/  外の世界との接続（SQLite、メール、Settings、pydantic の門）
  main.py          組み立て（コンポジションルート）
demos/             デモで使う「違反コード」。普段は ruff の対象外
```

## 準備

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

ruff check .        # All checks passed!
pyrefly check       # 0 errors
pytest -q           # 4 passed
```

> **注意**：Pyrefly は設定ファイルが無いと preset basic で動き、デモ①のエラーを出しません。
> このフォルダの pyproject.toml に `[tool.pyrefly]` が入っているので、このフォルダで実行してください。

## デモ①：Protocol は「形」で合う（2章）

```powershell
pyrefly check demos/app.py
```

HttpMailer は通り、FakeMailer だけが止まります。どちらも Mailer を import していません。

## デモ②：domain に sqlite3 を足すと（4章）

```powershell
copy demos\invoice_with_sqlite.py billing\domain\invoice.py
ruff check billing/domain/invoice.py
# TID251 `sqlite3` is banned: domain は DB を知らない
Remove-Item billing\domain\invoice.py
```

## デモ③：時計も止められる（4章）

```powershell
copy demos\pricing_today.py billing\domain\pricing_today.py
ruff check billing/domain/pricing_today.py
# TID251 `datetime.date.today` is banned: 今日の日付は引数で受け取る（第3回）
```

続けて、5章の「extend を忘れると黙る」を見せます。

```powershell
# billing/domain/ruff.toml の1行目（extend = ...）を消して保存
ruff check billing/domain/pricing_today.py
# All checks passed!   ← 守れているのではなく、見ていない
# extend の行を戻す
Remove-Item billing\domain\pricing_today.py
```

## 明日からの一歩：既存の違反を棚上げする

```powershell
copy demos\invoice_with_sqlite.py billing\domain\invoice.py
ruff check billing/domain/invoice.py --add-noqa
# import sqlite3  # noqa: TID251   ← 付いた noqa が、そのまま直す場所のリストになる
Remove-Item billing\domain\invoice.py
```

## アプリとして動かす（任意）

```powershell
python scripts/fake_mail_server.py    # 別のターミナルで
copy .env.example .env
python -m billing.main                # 請求書を発行しました: 2850円
Remove-Item .env, invoices.db
```

## 層ごとの禁止リスト

| 層 | ruff.toml | 禁止しているもの |
|---|---|---|
| domain | あり | billing.application, billing.infrastructure, sqlite3, requests, pydantic, date.today, os.environ |
| application | あり | billing.infrastructure, sqlite3, requests, date.today, os.environ |
| infrastructure | なし | （外側なので自由） |
| main.py | なし | （全部を組み立てる場所） |
