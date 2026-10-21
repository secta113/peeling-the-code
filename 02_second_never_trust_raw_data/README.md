# 第2回 講習会 デモ用コード

    pip install pyrefly pydantic

設定は `pyproject.toml` の `[tool.pyrefly]` に入っています。

| ページ | コマンド | 見せたいもの |
|---|---|---|
| 12 | `pyrefly check untyped.py` | `INFO 0 errors` ― 何も検査していない |
| 13 | `pyrefly check billing.py` | `float * None` を下線付きで指摘 |
| 14 | `pyrefly check billing.py` | 引数の取り違え 2件（22行目） |
| 15 | `pyproject.toml` の `preset` を切り替え | 厳しさは legacy / 既定 / strict の3段階 |
| 17 | `pyrefly check check.py` → `python check.py` | 怒られるが、実行すると 'abcabc' |
| 18 | `pyrefly check load_any.py` | `revealed type: Unknown` / `0 errors` |
| 19 | `python run_any.py` | `'15001500'` ― 落ちない |
| 23 | `python load_model.py` | `3000` ― 門を1枚通しただけ |
| 24 | `python load_broken.py` | 3件まとめての ValidationError |
| 26 | `pyrefly check typo.py`（①と②を切り替え） | dict は素通り / モデルは `Did you mean price?` |
| 27 | `python app.py` → `pyrefly check app.py` | append は素通り。静的側だけが捕まえる |
| 28 | `python stages.py` → `pyrefly check stages.py` | 段階ごとにモデルを分ける。飛ばすと止まる |
| 29 | `pyrefly check literal_demo.py` → `python literal_demo.py` | 同じ1行が両側で効く |
| 36 | `pyrefly init` | 既存の mypy / pyright 設定を読んで変換する |

`assignment_demo.py` は27ページの補足です。`validate_assignment=True` を付けると
再代入は止まりますが、`append` は止まらないことを確認できます。

## 原則（28ページ）

1. 一度作ったモデルは、足したり引いたりしない
2. 段階の数だけ、モデルを作る

途中で検証したいときは、その段階のモデルを作ります。書き換えるのではなく、次を作る。

構造で防ぐ手段:

- `list[Item]` → `tuple[Item, ...]` … `append` というメソッドが存在しなくなる
- `model_config = ConfigDict(frozen=True)` … 属性への代入を止める（append は止まらない）

## 補足

- 抑制コメントは `# type: ignore` がそのまま使えます（`# pyrefly: ignore` も可）
- 型注釈そのものは Python の標準仕様なので、mypy や Pyright に移っても書いた型は残ります
- 速度の参考値（300ファイル / 22,500行の合成コードで実測）: `pyrefly check` 0.36秒。
  本番前に、自分の環境・自分のコードで計り直してください

## pydantic と dataclass のコスト（実測 / Python 3.11・pydantic 2.13）

1件あたり:

| | 生成 | メモリ |
|---|---|---|
| dataclass | 134 ns | 104 B |
| pydantic BaseModel | 939 ns | 488 B |

1000件の JSON を読み込む:

| | 時間 |
|---|---|
| json.loads だけ（検査なし） | 0.40 ms |
| json.loads + 手書きの if 検査 + dataclass | +0.33 ms |
| pydantic を1件ずつ model_validate | 1.09 ms |
| pydantic TypeAdapter(list[Item]) | 0.56 ms |
| pydantic validate_json（JSON文字列から直接） | 0.75 ms |

`validate_json` は `json.loads` 自体を置き換えるので、境界で1回通すぶんには
手書きの検査とほぼ同じコストです。重いのは「内側で大量にモデルを作るとき」。

段階モデルのコスト:

| | 時間 |
|---|---|
| 入口で model_validate（dict から） | 1721 ns |
| 次の段へ（既存オブジェクトを渡す） | 1086 ns |
| 次の段へ（model_dump() を経由） | 3379 ns |

オブジェクトのまま渡せば中は再パースされないので、段階を分けても高くつきません。

その裏返しで、前の段で書き換えられた値は後段も素通りします。塞ぐなら
**内側のモデル**に `revalidate_instances="always"`（外側の器に付けても効きません）。
ただしコストは100件で 2.5 → 49 マイクロ秒と20倍になるので、全体には付けないこと。

なお `model_copy(update=...)` は検証しません。値の差し替えには使わないでください。
`model_construct`（検証をスキップする API）も速くなりません（実測 1966 ns）。
