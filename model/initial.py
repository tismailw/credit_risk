from pathlib import Path
import re
import pandas as pd
ROOT = Path("../kaggle/home-credit-credit-risk-model-stability")
TRAIN_DIR = ROOT / "csv_files" / "train"
TEST_DIR  = ROOT / "csv_files" / "test"

print("TEST_DIR:", TEST_DIR)

if not TEST_DIR.exists():
    raise FileNotFoundError(
        f"Directory not found: {TEST_DIR}\n"
        "Tip: If you're on Kaggle, ROOT should be "
        "'/kaggle/input/home-credit-credit-risk-model-stability'. "
        "If you're local, set ROOT to the folder where you downloaded the data."
    )
for p in sorted(TEST_DIR.glob("*.csv")):
    print(p)
