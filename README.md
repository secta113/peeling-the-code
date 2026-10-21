# Peeling the Code (peeling-the-code)

Pythonによるコード品質向上・テスト・型安全・アーキテクチャ設計の実践ハンズオン教材・デモコード集です。  
全4回の講習スライド（PowerPoint）と、各回の解説に対応した動作可能なPythonコードが含まれています。

---

## 目次と各章の概要

| ディレクトリ | テーマ / タイトル | 主なトピック・ツール |
|---|---|---|
| [`01_first_ruff_then_we_test`](./01_first_ruff_then_we_test/) | **第1回 テストコードと静的チェック** | `ruff` による複雑度検査、`pytest`、ゴールデンマスターテストによる安全なリファクタリング |
| [`02_second_never_trust_raw_data`](./02_second_never_trust_raw_data/) | **第2回 始める静的型チェック** | `pyrefly`（型チェッカー）、`pydantic`、外部データのバリデーション、段階的モデル遷移 |
| [`03_third_why_we_have_dependencies`](./03_third_why_we_have_dependencies/) | **第3回 外に繋ぐコードの依存関係の整理** | Before / After 比較、外部I/O（DB・外部API等）と業務ロジックの分離、テスタビリティの確保 |
| [`04_last_the_world_looks_like_an_onion`](./04_last_the_world_looks_like_an_onion/) | **第4回 依存の逆転_針に通せる形** | オニオンアーキテクチャ、依存性逆転の原則（DIP）、ドメイン層とインフラ層の分離、テスト容易性の極大化 |

---

## 使い方

各ディレクトリに移動し、それぞれの `README.md` の手順に従って環境構築・デモを実行してください。

```powershell
# 例: 第1回のデモを実行
cd 01_first_ruff_then_we_test
pip install ruff mypy pytest
ruff check billing.py
pytest -q
```
