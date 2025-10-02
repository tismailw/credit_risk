# Credit Risk Model Stability — Data Aggregation Notebook (`model.ipynb`)

This README documents the purpose and usage of the Jupyter notebook **`model.ipynb`**, which aggregates raw competition datasets into clean, analysis‑ready tables for the **Credit Risk Model Stability** project.

> Context: This project builds a customer‑level credit default risk model for the Home Credit competition with an emphasis on robustness under dataset shift.

---

## 📌 What this notebook does

- **Loads** the official Home Credit datasets (train/test and auxiliary tables).
- **Validates schema** and basic data types (IDs, dates, numeric features, categoricals).
- **Cleans** missing/erroneous values with reproducible rules.
- **Feature-level normalization** (optional): caps extreme outliers and applies simple transforms.
- **Aggregates & joins** auxiliary tables into a **single, denormalized dataframe** keyed by the primary identifier (e.g., `case_id` / `customer_id` — adjust to your dataset naming).
- **Exports** the unified tables to `./artifacts/` as Parquet/CSV for downstream modeling.
- **Logs** data quality (row/column counts, null rates, memory footprint).

---

## 🗂️ Repository layout (suggested)

```
/data/                  # raw CSV/Parquet downloaded from Kaggle (not committed)
/notebooks/
  model.ipynb           # THIS notebook: end-to-end aggregation
/src/
  utils_io.py           # I/O helpers (readers/writers with dtype hints)
  utils_agg.py          # feature aggregation and joins
  utils_qc.py           # data quality checks
/artifacts/
  train_agg.parquet     # aggregated training table (output)
  test_agg.parquet      # aggregated test table (output)
/README.md              # this file
```

> Note: Ensure large files (CSV/Parquet) and virtualenvs are **git‑ignored** (`.gitignore` includes `*.csv`, `*.parquet`, `.venv/`, `data/`, and `artifacts/`).

---

## 🔧 Prerequisites

- Python 3.10+
- JupyterLab/Notebook
- Recommended packages:
  - `pandas`, `numpy`, `pyarrow` (Parquet), `fastparquet` (optional), `tqdm`, `pyyaml`
  - `matplotlib` (for quick EDA visuals)
- Disk space: ~10–20 GB depending on extracted data

Install (example):
```bash
pip install -U pandas numpy pyarrow fastparquet tqdm pyyaml matplotlib
```

---

## 📥 Data sources

- Home Credit Credit Risk Model Stability datasets (download via Kaggle CLI or web).
- Place all raw files under `./data/` preserving original filenames.

Kaggle CLI example:
```bash
kaggle competitions download -c home-credit-credit-risk-model-stability -p data/
unzip data/home-credit-credit-risk-model-stability.zip -d data/
```

---

## ▶️ How to run

1. **Start Jupyter** in the project root:
   ```bash
   jupyter lab
   ```
2. Open **`notebooks/model.ipynb`**.
3. Update the **config cell** if paths or key column names differ in your copy:
   - `DATA_DIR`, `ARTIFACTS_DIR`
   - primary keys (e.g., `case_id`, `customer_id`), date columns, and categorical lists
4. **Run all cells** (Kernel → Restart & Run All).

Outputs (default):
- `artifacts/train_agg.parquet`
- `artifacts/test_agg.parquet`
- `artifacts/aggregation_report.json` (row counts, null rates, memory stats)

---

## 🧠 Key aggregation patterns

- **One-to-many → fixed width**: collapse child tables with groupby aggregations:
  - numeric: `mean`, `std`, `min`, `max`, `sum`, `last`
  - categorical: `nunique`, top‑k mode counts
  - temporal: recency features from last activity date
- **Cardinality control**: cap one‑hot features to top N categories; map the tail to `"__OTHER__"`.
- **Type safety**: apply `dtype` maps to avoid float‑ifying IDs.
- **Reproducibility**: keep the aggregation config (columns, reducers, thresholds) in `yaml` for versioning.

---

## ✅ Data quality checklist (automatic in notebook)

- Row counts preserved after joins
- No duplicate primary keys
- Expected column ranges (e.g., ages, amounts) sane
- Null rates within thresholds and documented
- Artifacts written atomically (write → fsync → rename)

---

## 🧪 Quick smoke test (after run)

```python
import pandas as pd
df = pd.read_parquet("artifacts/train_agg.parquet")
assert df.index.is_unique or df.iloc[:,0].is_unique  # primary key uniqueness
print(df.shape, df.isna().mean().round(4).head())
```

---

## 🚀 Next steps for modeling

- Baselines: Decision Tree / Logistic Regression
- Gradient boosting: LightGBM, XGBoost, CatBoost
- Stability diagnostics: out-of-time validation, PSI/CSI, temporal CV

> See the project plan for the staged model experiments and milestones.

---

## ⚠️ Troubleshooting

- **OOM / slow reads** → use `dtype` maps, chunked CSV, switch to Parquet, or increase `read_csv` `low_memory=False` with `chunksize`.
- **Mismatched keys** → strip/standardize key columns, check inner vs left join semantics.
- **Exploding columns** → limit high-cardinality one‑hots; prefer target/impact encoding (with leakage guards).

---

## 📄 License & attribution

- Data © respective owners (Home Credit / Kaggle terms).
- Code in this repo under MIT.
- Please cite the competition and any external write‑ups you borrowed ideas from.

---

*Maintainer:* Tahir Ismailwala (and team)  
*Notebook:* `notebooks/model.ipynb`  
*Outputs:* `artifacts/*.parquet`, `artifacts/aggregation_report.json`

