# 講習デモ用コード一式

スライド 13〜32 で映すデモの実物です。そのまま順番に打てば、スライドと同じ出力が出ます。

## 準備

```powershell
pip install ruff mypy pytest
```

## ファイル

| ファイル | 役割 |
|---|---|
| `billing.py` | リファクタリング前の長い関数（複雑度17・分岐18） |
| `billing_v2.py` | リファクタリング後（差し替え用） |
| `test_golden_master.py` | ゴールデンマスターテスト |
| `test_billing.py` | 分割後のユニットテスト（v2 に差し替えてから実行） |
| `pyproject.toml` | 複雑度ルールを有効化した ruff 設定 |

## デモの順番

### ① 既定の ruff は何も言わない（スライド13）

```powershell
ruff check --isolated billing.py
# → All checks passed!
```

### ② 複雑度ルールを有効化すると指摘される（スライド15）

```powershell
ruff check billing.py     # pyproject.toml の設定が効く
# → C901 `calc_invoice` is too complex (17 > 10)
# → PLR0912 Too many branches (18 > 12)
```

### ③ ゴールデンマスターを作る（スライド23）

```powershell
del golden_master.json    # やり直すとき用
pytest -q                 # 1回目: 324ケースを記録
pytest -q                 # 2回目以降: 記録と比較（1 passed, 1 skipped）
```

### ④ バグを入れると落ちる（スライド24）

`billing.py` の `total * 0.90` を `total * 0.91` に書き換えて：

```powershell
pytest -q
# → 'output': 3923} != 'output': 3895}
```

書き戻すと緑に戻ります。

### ⑤ すり抜けるバグもある（スライド25）

`billing_v2.py` に差し替えてから、`FREE_SHIPPING_THRESHOLD` を `10001` にする。

```powershell
copy billing_v2.py billing.py
del golden_master.json
pytest -q                 # まずゴールデンマスターを作り直す
# ここで 10000 → 10001 に書き換えて
pytest -q
# → 通ってしまう（324ケースに「ちょうど10000円」がないため）
```

### ⑥ 境界値を足すと捕まる（スライド26）

`test_golden_master.py` の `item_sets` に1行足す：

```python
[{"category": "other", "price": 10000, "qty": 1}],
```

```powershell
del golden_master.json
pytest -q                 # 432ケースで作り直す
# 同じバグを入れると → At index 423 diff: 'output': 12530} != 'output': 11330}
```

### ⑦ 分割後はユニットテストが書ける（スライド31〜32）

```powershell
copy billing_v2.py billing.py
pytest -q
# → 13 passed
```

## ハマりどころ

`billing.py` を差し替えても結果が変わらないときは、`__pycache__` を消してください。
ファイルサイズが同じで書き換えが同じ秒内に起きると、古い `.pyc` が使われることがあります。

```powershell
rmdir /s /q __pycache__
```
