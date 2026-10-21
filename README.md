# Peeling the Code (peeling-the-code)

Pythonによるコード品質向上・テスト・型安全・アーキテクチャ設計の実践ハンズオン教材・デモコード集です。  
全4回の講習スライド（PowerPoint）と、各回の解説に対応した動作可能なPythonコードが含まれています。

---

## 請求システム（Billing）が辿る進化の物語

本教材のコードは、全4回を通して **「請求書計算（Billing）」という同一の業務ドメイン** を題材にしています。  
回を追うごとに、コードが直面する課題とアーキテクチャが劇的に進化していくプロセスを体感できます。

```
第1回【泥団子からの脱出】
  └── 1つの長大な関数（複雑度17）。
      ゴールデンマスターテストで振る舞いを保護し、安全に関数分割リファクタリング。
        ↓
第2回【生データと境界の防壁】
  └── 分割されたロジックに潜む「型の欠落」と「外部データの罠」。
      Pydanticと静的型チェック（pyrefly）を導入し、境界（門）で生データを弾く。
        ↓
第3回【外部世界との戦いとDI】
  └── DB保存・メール送信・時計など「外の世界」と繋がった途端にテスト不能に。
      Protocol（インターフェース）と依存性注入（DI）で外部依存を切り離す。
        ↓
第4回【オニオンアーキテクチャ】
  └── ドメイン層を中心に据え、依存の向きを機械的（ruff）に強制。
      外側の都合（DB・API等）に一切汚されない、極限までテスト容易な設計へ。
```

---

## 目次と各章の構成

| ディレクトリ | テーマ / タイトル | 構成 | 主なトピック・ツール |
|---|---|---|---|
| [`01_first_ruff_then_we_test`](./01_first_ruff_then_we_test/) | **第1回 テストコードと静的チェック** | `before/`（旧コード）<br>`after/`（分割後） | `ruff` による複雑度検査、`pytest`、ゴールデンマスターテストによる安全なリファクタリング |
| [`02_second_never_trust_raw_data`](./02_second_never_trust_raw_data/) | **第2回 始める静的型チェック** | `01_types/`<br>`02_raw_data/`<br>`03_pydantic/`<br>`04_stages/` | `pyrefly`（型チェッカー）、`pydantic`、外部データのバリデーション、段階的モデル遷移 |
| [`03_third_why_we_have_dependencies`](./03_third_why_we_have_dependencies/) | **第3回 外に繋ぐコードの依存関係の整理** | `before/`（密結合）<br>`after/`（疎結合）<br>`scripts/`（デモ環境） | Before / After 比較、外部I/O（DB・メールAPI等）と業務ロジックの分離、Protocol による DI |
| [`04_last_the_world_looks_like_an_onion`](./04_last_the_world_looks_like_an_onion/) | **第4回 依存の逆転_針に通せる形** | `billing/`（層別）<br>`demos/`<br>`tests/` | オニオンアーキテクチャ、依存性逆転の原則（DIP）、ドメイン層とインフラ層の分離、`ruff.toml` による依存方向の自動検査 |

---

## 環境構築と使い方

各章は独立した演習ディレクトリとなっています。試したい章のディレクトリに移動し、`venv` を作成してデモを実行してください。

```powershell
# 例: 第1回のデモを実行する場合
cd 01_first_ruff_then_we_test

# 仮想環境の作成と有効化
python -m venv .venv
.venv\Scripts\Activate.ps1

# 依存パッケージのインストール（全章でバージョン固定）
pip install -r requirements-dev.txt

# 各章の README.md に従ってデモを実行
cd before
ruff check billing.py
pytest -q
```
