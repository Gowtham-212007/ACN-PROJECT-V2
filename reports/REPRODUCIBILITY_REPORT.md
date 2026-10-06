# Reproducibility Report

- Environment: Python 3, numpy, pandas, scikit-learn>=1.4, scipy, joblib, matplotlib, pytest (see `requirements.txt`).
- Seed: 42 everywhere (`src/acn/config.py`); folds are deterministic via `RepeatedStratifiedKFold`.
- Data: `data/sample.npz` (1000 x 78, 11 classes) committed; raw CSVs are not (registration required at the CIC site).
- Commands: see `RUN_EXPERIMENTS.md`. Raw outputs are timestamped CSV/JSON in `results/raw/`; tables and figures are regenerated from them only.
- Tests: `pytest tests/` (3 pass) checks leakage-free fitting, metric calculation and space enumeration.
- Not reproducible from this repo alone: the sample's construction (needs raw data); runtime numbers depend on the CPU (single machine, serial, median of 5).
- Known non-determinism: none observed for the cached sample; KPCA eigen-solver is `auto` and seeded.
- Paper build: needs the real `IEEEtran.cls`; the PDF in the repo is a layout preview using a shim class.
