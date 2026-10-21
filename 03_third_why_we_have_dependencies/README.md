# 第3回 デモコード：外に繋がるコードの依存症の治し方

スライドの各デモを、この順で実行します。コマンドは PowerShell 前提です。

```
before/   治療前（患者のコード）
after/    治療後（DI と pydantic-settings）
scripts/  デモの舞台装置（偽メールサーバー、「自分の PC」の再現）
```

## 準備

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

別のターミナルで偽メールサーバーを起動しておきます（before/ のコードは「本番のメール API」としてここに送ります）。

```powershell
python scripts/fake_mail_server.py
```

> before/billing.py のキャンペーン最終日は `2026-11-30` です。講習の日がそれより後なら、
> before/billing.py と after/billing/invoice.py の日付を講習日より後に変えてください（デモ①が落ちる理由が変わってしまうため）。

## デモ①：テストを書いてみる（2章）

```powershell
cd before
python ../scripts/setup_my_pc.py      # 「自分の PC」：C:/billing/prod.db を作る
pytest -q                             # 1 passed
python ../scripts/count_invoices.py   # 本番 DB に請求書が1件増えている
                                      # 偽メールサーバーの画面に「メール送信」が出ている

python ../scripts/teardown_my_pc.py   # 「他の人の PC」：C:/billing を消す
pytest -q                             # sqlite3.OperationalError: unable to open database file
cd ..
```

見せどころは「通ったとき」の方です。本番 DB に書き込み、本物のメールを送っています。

## デモ②：形を間違えた偽物を渡す（3章 Step 2）

```powershell
cd after
pyrefly check demos/wrong_fake.py
```

`FakeMailer` is not assignable to parameter `mailer` with type `Mailer` が出ます。

> **注意**：Pyrefly は設定ファイル（pyproject.toml の `[tool.pyrefly]` か pyrefly.toml）が無いと
> preset basic で動き、このエラーを出しません。after/ には設定が入っているので、after/ の中で実行してください。

## デモ③：テストでは偽物を渡す ／ デモ④：境界値（3章 Step 3）

```powershell
pytest -q                             # 3 passed（DB もネットワークも不要）
```

tests/test_invoice.py の `FakeMailer.send` から引数を消すと、デモ②と同じエラーがテストファイルでも出ます。

## 4章：os.environ を関数の奥で読むと、途中で落ちる

```powershell
cd ../before
$env:DB_PATH = "env_demo.db"
Remove-Item Env:MAIL_API_URL -ErrorAction SilentlyContinue
python env_style.py
# 請求額を計算しました: 2850
# DB に保存しました: A-1042
# KeyError: 'MAIL_API_URL'
Remove-Item env_demo.db
cd ../after
```

## デモ⑤：壊れた設定は、起動時に止まる（4章）

```powershell
copy .env.broken .env
python main.py                        # 3 validation errors for Settings（計算も保存も始まらない）

copy .env.example .env
python main.py                        # 請求書を発行しました: 2850円（偽メールサーバーに届く）
Remove-Item .env, invoices.db
```

## ファイルとスライドの対応

| ファイル | スライド |
|---|---|
| before/billing.py | 患者のコード、診断結果 |
| after/billing/invoice.py | Step 1：隠れた依存を、引数に出す |
| after/billing/ports.py | Step 2：Protocol |
| after/tests/test_invoice.py | Step 3：偽物を渡す、境界値 |
| after/billing/infra.py, after/main.py | Step 4：組み立ては一番外側だけ |
| after/billing/settings.py | pydantic-settings で、入口に門を立てる |
