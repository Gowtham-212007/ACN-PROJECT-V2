# Running the experiments

```bash
pip install -r requirements.txt
pytest tests/                                   # sanity checks
python -m src.acn.run_cv --smoke                # ~1 min pipeline check
python -m src.acn.run_cv --n-jobs 4             # full grid on data/sample.npz
python -m src.acn.run_sizes && python -m src.acn.run_runtime
python -m src.acn.stats_tests
python -m src.acn.run_nested --repeats 3 --n-jobs 2   # nested CV (~6.5 min on 2 cores)
python -m src.acn.analyze_nested                       # nested tables + T11
python -m src.acn.check_claims                         # recompute every paper number from raw files
python -m src.acn.make_tables && python -m src.acn.make_figures
```

## Experiments needing the raw dataset (NOT run by the authors of this branch)
1. Download CIC-IDS2017 *MachineLearningCVE* CSVs from the University of New Brunswick CIC website.
2. `python -m src.acn.prepare_raw <csv_dir>` builds a sample with train-only imputation.
3. `python -m src.acn.run_cv --data <new_npz>` repeats the grid; `python -m src.acn.run_temporal <csv_dir>` runs the day-wise split.
4. Re-run stats/tables/figures, then update numbers in `papers/ieee/IEEE_ACCESS_FINAL.tex` (check with `python -m src.acn.check_claims` and `papers/ieee/FINAL_NUMERICAL_AUDIT.md`).

Paper: `papers/ieee/build_access.sh` compiles `IEEE_ACCESS_FINAL.tex` with the official IEEE Access template (files in `papers/ieee/ieeeaccess/`); fill the `TO BE FILLED` fields first.


## v2 (raw data) commands
```
export ACN_RUN=v2
python -m src.acn.profile_raw <RAW_DIR>
python -m src.acn.prepare_raw <RAW_DIR> --n 6000 --min-per-class 100 --out data/sample_raw6000.npz
python -m src.acn.run_cv --data data/sample_raw6000.npz
python -m src.acn.run_nested; python -m src.acn.stats_tests; python -m src.acn.analyze_nested
python -m src.acn.run_tuning; python -m src.acn.run_temporal; python -m src.acn.run_blocked
python -m src.acn.run_runtime; python -m src.acn.run_sizes
python -m src.acn.analyze_extra; python -m src.acn.make_tables; python -m src.acn.make_figures
python -m src.acn.check_claims
```
v1 (1,000-row) outputs are preserved under the default (unset ACN_RUN) paths and `papers/ieee/archive/`.
