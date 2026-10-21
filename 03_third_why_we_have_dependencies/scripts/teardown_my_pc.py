"""デモ用：「他の人の PC」を再現する。setup_my_pc.py で作った C:/billing を消す。

使い方: python scripts/teardown_my_pc.py
"""

import shutil
from pathlib import Path

DIR = Path("C:/billing")

if __name__ == "__main__":
    shutil.rmtree(DIR, ignore_errors=True)
    print(f"削除しました: {DIR.resolve()}")
