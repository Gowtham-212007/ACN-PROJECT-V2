# Verifying and re-running the paper's experiments

```bash
pip install -r requirements.txt
export ACN_RUN=v2                                  # all paper results live in results/v2/
pytest tests/                                      # sanity checks
python -m src.acn.check_claims                     # recompute every number in the paper from results/v2/raw; expects 232/232 PASS
```

## Re-run everything (needs the raw CIC-IDS2017 MachineLearningCVE CSVs)
Download the eight daily CSV files from the Canadian Institute for Cybersecurity, then:
```bash
export ACN_RUN=v2
python -m src.acn.profile_raw <RAW_DIR>
python -m src.acn.prepare_raw <RAW_DIR> --n 6000 --min-per-class 100 --out data/sample_raw6000.npz   # seed 0
python -m src.acn.run_cv --data data/sample_raw6000.npz
python -m src.acn.run_nested; python -m src.acn.stats_tests; python -m src.acn.analyze_nested
python -m src.acn.run_tuning; python -m src.acn.run_temporal; python -m src.acn.run_blocked
python -m src.acn.run_runtime; python -m src.acn.run_sizes
python -m src.acn.analyze_extra; python -m src.acn.make_tables; python -m src.acn.make_figures
python -m src.acn.check_claims
```
`data/sample_raw6000.npz` and its manifest are included, so the cross-validation, statistics and claim checks can be re-run without the raw files. The raw files are only needed to rebuild the sample.
