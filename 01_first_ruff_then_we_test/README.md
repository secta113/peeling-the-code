# 第1回 講習デモ用コード：テストコードと静的チェック

スライド 14〜35 で映すデモの実物です。そのまま順番に打てば、スライドと同じ出力が出ます。

```
before/   リファクタリング前（複雑度17の長い関数、ゴールデンマスター）
after/    リファクタリング後（関数分割後、境界値入りのゴールデンマスター、ユニットテスト）
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

#### ① 既定の ruff は何も言わない（スライド14）

```powershell
ruff check --isolated billing.py
# → All checks passed!
```

#### ② 複雑度ルールを有効化すると指摘される（スライド16）

```powershell
ruff check billing.py     # pyproject.toml の設定が効く
# → C901 `calc_invoice` is too complex (17 > 10)
# → PLR0912 Too many branches (18 > 12)
```

#### ③ ゴールデンマスターを作る（スライド26）

```powershell
del golden_master.json    # やり直すとき用
pytest -q                 # 1回目: 324ケースを記録
pytest -q                 # 2回目以降: 記録と比較（1 passed, 1 skipped）
```

#### ④ バグを入れると落ちる（スライド27）

`billing.py` の `total * 0.90` を `total * 0.91` に書き換えて：

```powershell
pytest -q
# → 'output': 3923} != 'output': 3895}
```

確認後、元の `total * 0.90` に戻すと緑に戻ります。

#### ⑤ すり抜けるバグもある（スライド28）

`billing.py` の `if total >= 10000:` を `10001` に書き換えて：

```powershell
pytest -q
# → 1 passed, 1 skipped（通ってしまう。324ケースに「ちょうど10000円」がないため）
```

確認後、`10000` に戻します。
バグが入ったまま次の⑥で作り直すと、バグ込みの出力が「正解」として記録されてしまいます。

#### ⑥ 境界値を足すと捕まる（スライド29）

`test_golden_master.py` の `item_sets` に1行足す：

```python
[{"category": "other", "price": 10000, "qty": 1}],
```

```powershell
del golden_master.json
pytest -q                 # 432ケースで作り直す（2 passed）
```

ここで同じバグ（`10000` → `10001`）を入れると捕まります：

```powershell
pytest -q
# → At index 423 diff: 'output': 12530} != 'output': 11330}
```

確認後、`10000` に戻します。ここで記録した432ケースを、⑦でリファクタリング後のコードと照合します。

---

### 【後半】after/ での体験（リファクタリングとユニットテスト）

after/ の `test_golden_master.py` には、⑥で足した境界値の行が最初から入っています。

```powershell
cd ../after
```

#### ⑦ 分割後も振る舞いが変わっていないことを確認（スライド33）

before/ で記録したゴールデンマスターを持ってきて、分割後のコードと照合します。
ここで作り直すと分割後の出力を記録し直すだけになり、何も確かめられません。

```powershell
ruff check billing.py
# → All checks passed!（複雑度の指摘が消えた）
copy ..\before\golden_master.json .
pytest -q test_golden_master.py
# → 1 passed, 1 skipped（432ケースすべて1円も変わっていない）
```

#### ⑧ 分割後は小さく読めるユニットテストが書ける（スライド35）

```powershell
pytest -q test_billing.py
# → 11 passed
```

---

## ハマりどころ

書き換えたのに結果が変わらないときは、`__pycache__` を消してください。
ファイルサイズが同じまま（`0.90` → `0.91`、`10000` → `10001`）同じ秒のうちに保存し直すと、
古い `.pyc` が使われることがあります。

```powershell
rmdir /s /q __pycache__
```
