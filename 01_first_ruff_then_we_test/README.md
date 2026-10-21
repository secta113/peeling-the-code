# 第1回 講習デモ用コード：テストコードと静的チェック

スライド 13〜32 で映すデモの実物です。そのまま順番に打てば、スライドと同じ出力が出ます。

```
before/   リファクタリング前（複雑度17の長い関数、ゴールデンマスター）
after/    リファクタリング後（関数分割後、ゴールデンマスター維持、ユニットテスト）
```

## 準備

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

---

## デモの手順

### 【前半】before/ での体験（現状把握と保護）

```powershell
cd before
```

#### ① 既定の ruff は何も言わない（スライド13）

```powershell
ruff check --isolated billing.py
# → All checks passed!
```

#### ② 複雑度ルールを有効化すると指摘される（スライド15）

```powershell
ruff check billing.py     # pyproject.toml の設定が効く
# → C901 `calc_invoice` is too complex (17 > 10)
# → PLR0912 Too many branches (18 > 12)
```

#### ③ ゴールデンマスターを作る（スライド23）

```powershell
del golden_master.json    # やり直すとき用
pytest -q                 # 1回目: 324ケースを記録
pytest -q                 # 2回目以降: 記録と比較（1 passed, 1 skipped）
```

#### ④ バグを入れると落ちる（スライド24）

`billing.py` の `total * 0.90` を `total * 0.91` に書き換えて：

```powershell
pytest -q
# → 'output': 3923} != 'output': 3895}
```

確認後、元の `total * 0.90` に戻すと緑に戻ります。

---

### 【後半】after/ での体験（リファクタリングとユニットテスト）

```powershell
cd ../after
```

#### ⑤ 分割後も振る舞いが変わっていないことを確認（スライド25）

```powershell
del golden_master.json
# before で作ったゴールデンマスターを検証、または作り直す
pytest -q test_golden_master.py
# → 1 passed, 1 skipped
```

#### ⑥ すり抜けるバグの体験（スライド25）

`billing.py` の `FREE_SHIPPING_THRESHOLD` を `10000` から `10001` に書き換えて実行：

```powershell
pytest -q test_golden_master.py
# → 通ってしまう（324ケースに「ちょうど10000円」がないため）
```

#### ⑦ 境界値を足すと捕まる（スライド26）

`test_golden_master.py` の `item_sets` に1行足す：

```python
[{"category": "other", "price": 10000, "qty": 1}],
```

```powershell
del golden_master.json
pytest -q test_golden_master.py    # 432ケースで作り直す
# 同じバグ（10001）を入れると → At index 423 diff: 'output': 12530} != 'output': 11330}
```

確認後、`billing.py` の `FREE_SHIPPING_THRESHOLD` を `10000` に戻します。

#### ⑧ 分割後は小さく読めるユニットテストが書ける（スライド31〜32）

```powershell
pytest -q test_billing.py
# → 13 passed
```
