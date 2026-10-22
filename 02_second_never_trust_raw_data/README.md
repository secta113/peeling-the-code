# 第2回 講習会 デモ用コード：始める静的型チェック

スライドの進行に合わせて、4つのディレクトリにコードを整理しています。  
コマンドはすべてこのディレクトリ（`02_second_never_trust_raw_data`）直下から実行してください。

```
01_types/     【基礎】型なしの恐怖と静的型チェック
02_raw_data/  【境界】生データとAnyの落とし穴
03_pydantic/  【防壁】Pydanticによるバリデーション
04_stages/    【発展】段階的モデルとイミュータビリティ
models.py     各ディレクトリから共通で使う Order / Item モデル
```

`python` は `python -m 01_types.check` のようにモジュール名で実行します。
`python 01_types/check.py` の形だと直下が import の検索先に入らず、`models` が見つかりません。

## 準備

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

設定は `pyproject.toml` の `[tool.pyrefly]` に入っています。

---

## デモ一覧（スライド対応表）

| ページ | テーマ / 対象 | コマンド | 見せたいもの |
|---|---|---|---|
| 12 | **01_types** | `pyrefly check 01_types/untyped.py` | `INFO 0 errors` ― 型がないと何も検査できない |
| 13 | **01_types** | `pyrefly check 01_types/billing.py` | `float * None` を下線付きで指摘（第1回のコード） |
| 14 | **01_types** | `pyrefly check 01_types/billing.py` | 引数の取り違え 2件（22行目） |
| 15 | 設定切替 | `pyproject.toml` の `preset` を切り替え | 厳しさは legacy / 既定 / strict の3段階 |
| 17 | **01_types** | `pyrefly check 01_types/check.py`<br>`python -m 01_types.check` | 怒られるが、実行すると 'abcabc'（静的と実行時のズレ） |
| 18 | **02_raw_data** | `pyrefly check 02_raw_data/load_any.py` | `revealed type: Any` / `0 errors`（Any は沈黙する） |
| 19 | **02_raw_data** | `python -m 02_raw_data.run_any` | `'15001500'` ― 文字列のまま足し算されて落ちない |
| 23 | **03_pydantic** | `python -m 03_pydantic.load_model` | `3000` ― 門（Pydantic）を1枚通しただけで安全になる |
| 24 | **03_pydantic** | `python -m 03_pydantic.load_broken` | 3件まとめての ValidationError |
| 26 | **03_pydantic** | `pyrefly check 03_pydantic/typo.py`（①と②を切り替え） | dict は素通り / モデルは `Did you mean price?` |
| 27 | **04_stages** | `python -m 04_stages.app`<br>`pyrefly check 04_stages/app.py` | append は実行時は素通り。静的側だけが捕まえる |
| 28 | **04_stages** | `python -m 04_stages.stages`<br>`pyrefly check 04_stages/stages.py` | 段階ごとにモデルを分ける。飛ばすと止まる |
| 29 | **01_types** | `pyrefly check 01_types/literal_demo.py`<br>`python -m 01_types.literal_demo` | Literal型：同じ1行が両側で効く |
| 36 | 移行ツール | `pyrefly init` | 既存の設定を読んで変換する |

> `04_stages/assignment_demo.py`（`python -m 04_stages.assignment_demo`）は27ページの補足です。`validate_assignment=True` を付けると再代入は止まりますが、`append` は止まらないことを確認できます。

---

## 原則（28ページ）

1. **一度作ったモデルは、足したり引いたりしない**
2. **段階の数だけ、モデルを作る**

途中で検証したいときは、その段階のモデルを作ります。書き換えるのではなく、次を作る。

### 構造で防ぐ手段:
- `list[Item]` → `tuple[Item, ...]` … `append` というメソッドが存在しなくなる
- `model_config = ConfigDict(frozen=True)` … 属性への代入を止める（append は止まらない）

---

## 補足

- 抑制コメントは `# type: ignore` がそのまま使えます（`# pyrefly: ignore` も可）
- 型注釈そのものは Python の標準仕様なので、他の型チェッカーに移っても書いた型はそのまま活きます
- 速度の参考値（300ファイル / 22,500行の合成コードで実測）: `pyrefly check` 0.36秒。本番前に、自分の環境・自分のコードで計り直してください

---

## pydantic と dataclass のコスト（実測 / Python 3.11・pydantic 2.13）

### 1件あたり:
| | 生成 | メモリ |
|---|---|---|
| dataclass | 134 ns | 104 B |
| pydantic BaseModel | 939 ns | 488 B |

### 1000件の JSON を読み込む:
| | 時間 |
|---|---|
| json.loads だけ（検査なし） | 0.40 ms |
| json.loads + 手書きの if 検査 + dataclass | +0.33 ms |
| pydantic を1件ずつ model_validate | 1.09 ms |
| pydantic TypeAdapter(list[Item]) | 0.56 ms |
| pydantic validate_json（JSON文字列から直接） | 0.75 ms |

`validate_json` は `json.loads` 自体を置き換えるので、境界で1回通すぶんには手書きの検査とほぼ同じコストです。重いのは「内側で大量にモデルを作るとき」。

### 段階モデルのコスト:
| | 時間 |
|---|---|
| 入口で model_validate（dict から） | 1721 ns |
| 次の段へ（既存オブジェクトを渡す） | 1086 ns |
| 次の段へ（model_dump() を経由） | 3379 ns |

オブジェクトのまま渡せば中は再パースされないので、段階を分けても高くつきません。  
その裏返しで、前の段で書き換えられた値は後段も素通りします。塞ぐなら**内側のモデル**に `revalidate_instances="always"`（外側の器に付けても効きません）。ただしコストは100件で 2.5 → 49 マイクロ秒と20倍になるので、全体には付けないこと。

なお `model_copy(update=...)` は検証しません。値の差し替えには使わないでください。  
`model_construct`（検証をスキップする API）も速くなりません（実測 1966 ns）。
