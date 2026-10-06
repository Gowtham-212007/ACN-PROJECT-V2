# Running the experiments

```bash
pip install -r requirements.txt
pytest tests/                                   # sanity checks
python -m src.acn.run_cv --smoke                # ~1 min pipeline check
python -m src.acn.run_cv --n-jobs 4             # full grid on data/sample.npz
python -m src.acn.run_sizes && python -m src.acn.run_runtime
python -m src.acn.stats_tests
python -m src.acn.make_tables && python -m src.acn.make_figures
```

## Experiments needing the raw dataset (NOT run by the authors of this branch)
1. Download CIC-IDS2017 *MachineLearningCVE* CSVs from the University of New Brunswick CIC website.
2. `python -m src.acn.prepare_raw <csv_dir>` builds a sample with train-only imputation.
3. `python -m src.acn.run_cv --data <new_npz>` repeats the grid; `python -m src.acn.run_temporal <csv_dir>` runs the day-wise split.
4. Re-run stats/tables/figures, then update numbers in `papers/ieee/paper.tex` (check against `CLAIM_AUDIT.md`).

Paper: copy `papers/ieee/` to Overleaf (real IEEEtran), fill in author block, compile `paper.tex`.
