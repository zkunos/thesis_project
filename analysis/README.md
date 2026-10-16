# Reproducible clustering extension

Run from the repository root using Python 3.12 and the packages pinned in `requirements-research.lock.txt`. The local execution used `.venv-research/Scripts/python.exe`.

```powershell
python -m venv .venv-research
.\.venv-research\Scripts\python.exe -m pip install -r analysis/requirements-research.lock.txt
.\analysis\run_research.ps1
```

Use a Python 3.12 interpreter for the first command. If the environment was created from the bundled runtime without pip, install from an existing pip-enabled Python with `python -m pip --python .\.venv-research\Scripts\python.exe install -r analysis/requirements-research.lock.txt`.

The driver executes preparation, original-space benchmarks, missing-data mixtures, independent imputation ensembles, ensemble aggregation, continuous-reference simulations, preprocessing sensitivity, exploratory scaling checks, patient trajectories and reporting. It then runs numerical validation and checks input/output hashes, assignment joins, completed model grids and notebook source syntax. NB15–NB17 are thin notebook entry points for the same scripts. `run_all.sh` continues to represent the historical pipeline.

For individual stages:

```powershell
.\.venv-research\Scripts\python.exe -m analysis.run_research --stage benchmark
.\.venv-research\Scripts\python.exe -m analysis.run_research --stage robust --family t4
.\.venv-research\Scripts\python.exe -m analysis.test_research
```

Available stages: `prepare`, `benchmark`, `robust`, `ensemble`, `aggregate`, `calibration`, `sensitivity`, `scaling`, `trajectory`, `report`. Run preparation first. Aggregation and scaling depend on the completed ensemble stage. Reporting requires all output tables. Robust families can run concurrently because each writes separate files. Default robust execution recomputes its grid. `--resume` is only for an interrupted grid with identical inputs and configuration; it must not be used to reuse outputs after changes.

New outputs go to `results/research_2026/`; generated figures and the report go to `report/research/`. Intermediate caches contain patient-level data and remain local. Results are ignored by the repository's existing generated-data rule; the source and aggregate report are trackable. Model pickle/joblib files are local analysis artifacts and should only be loaded from trusted sources.

The domain transformer has two interfaces. `CognitivePreprocessor.fit()` learns parameters from discovery patients and `.transform_tests()` applies them to another cohort. The `compute_domain_scores()` compatibility wrapper fits on the supplied complete dataset to reproduce legacy NB5 behavior. New validation analyses must use the fitted transformer, not fit the compatibility wrapper on validation patients.

Model conventions: native missing-data mixtures use fixed t degrees of freedom or fixed contamination parameters, with covariance eigenvalues bounded below; all likelihoods integrate missing coordinates. Sampled PAM optimizes medoids within three subsamples. The trajectory model integrates patient random intercepts and slopes and shares their covariance across latent classes. These choices are explicit approximations and are not exact reproductions of the cited software.

The run records source-file hashes, extract-scoped assessment keys, a frozen patient split, dependency versions and aggregate results. The data do not include a verified natural assessment/episode key or an independent functional outcome. See the generated results report for convergence limits, sensitivity findings and interpretation.
