# CogDash 2.0

Local research dashboard for the saved acquired-brain-injury clustering analyses. It presents 11 pages, including patient-level repeatability, original-space model comparisons, scaling sensitivity, and longitudinal results. The assessment-level and patient-level analyses retain separate interpretations.

## Start in this workspace

The research environment and dashboard assets have been prepared here. From the repository root in PowerShell:

```powershell
./dashboard/run.ps1
```

Open <http://127.0.0.1:8501>. Stop the server with Ctrl+C. If the port is already occupied, reuse the existing CogDash instance or run `./dashboard/run.ps1 -Port 8502`.

The equivalent direct command, run from `dashboard/`, is:

```powershell
../.venv-research/Scripts/python.exe -m streamlit run Home.py --server.address 127.0.0.1 --server.port 8501 --server.fileWatcherType none
```

The application binds to the local machine. Restart it after changing source or results; source watching is disabled and saved data are cached for the life of the process.

## Set up a fresh environment

Use Python 3.12 and the project's existing generated results. A source checkout alone does not include the ignored `results/` directory.

```powershell
py -3.12 -m venv .venv-research
./.venv-research/Scripts/python.exe -m pip install -r analysis/requirements-research.lock.txt
./.venv-research/Scripts/python.exe -m pip install -r dashboard/requirements.txt
./.venv-research/Scripts/python.exe -m dashboard.export_data
./dashboard/run.ps1
```

Run those commands from the repository root. The full research dependencies are needed to deserialize the saved experiment models during asset preparation. The server itself reads a compact saved model; it does not retrain the experiments. Use only trusted project model files, since pickle/joblib loading executes Python object reconstruction.

Required local inputs include:

- Assessment-level tables and serialized outputs in `results/`, including `shared_infrastructure.pkl`, the hypothesis summaries, feature importance, and stability results.
- Patient-level tables, `prepared.joblib`, and `benchmarks.joblib` in `results/research_2026/`.
- `results/eda_output.pkl` and `data/0_UNITATM.xlsx` to prepare aggregate clinical-unit tables.

`python -m dashboard.export_data` verifies the saved two- and three-group k-means assignments, exports a compact inference model without patient identifiers, generates validation-profile and clinical-unit aggregates, and records source hashes in `results/dashboard/source_manifest.json`. It does not fit new models. If the underlying analyses change, regenerate these assets and restart the server.

## Pages and interpretation

| Area | Pages |
| --- | --- |
| Findings | Home; Patient-Level Research |
| Explore | Cluster Explorer; Cognitive Profiles; Patient Lookup; New Profile |
| Compare | Imputation Compare; Clinical Units; Hypothesis Summary; Advanced Analytics; Robustness |

The patient-level analysis uses 5,828 discovery and 1,457 validation patients. K-means two-group agreement across 20 independent imputation fits is ARI 0.959; three-group agreement is 0.935. Robust versus equal-domain three-group scaling gives ARI 0.243. These results support repeatable partitions under specified choices, without establishing discrete clinical phenotypes. The trajectory selection rule retains one class among 2,013 patients.

Patient Lookup starts with an explicitly synthetic example; disabling that option permits local assessment-row lookup. New Profile accepts raw test scores, applies fixed discovery preprocessing and the saved two- or three-group model, and reports distances rather than probabilities. Blank scores are imputed. No diagnostic or treatment validity is established.

Tables use escaped semantic HTML for portability. Plotly supplies interactive charts and plot downloads. The 3D view requires browser WebGL support. The fixed t-SNE projection is recolored across partitions; the UMAP coordinates change with imputation method.

## Validation and manual

```powershell
./.venv-research/Scripts/python.exe -m unittest dashboard.tests.test_dashboard -v
```

Functional tests cover all 11 pages, saved-data consistency, predictions against saved validation assignments, missing/nonfinite input, method changes, empty group selection, and the profile form. Browser verification and captures additionally cover the rendered charts and a synthetic complete profile.

The [manual source](../presentation/cogdash_manual.tex) and [PDF manual](../presentation/cogdash_manual.pdf) document the recreated interface. Fifteen actual browser captures are in `presentation/manual_screenshots/`; the capture manifest records page state, dates, and hashes. Screenshots use synthetic examples for individual profiles.
