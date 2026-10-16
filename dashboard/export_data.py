"""Prepare compact local dashboard assets from the executed analysis.

Run from the repository root: python -m dashboard.export_data
No models are fitted and no patient identifiers are exported to the model bundle.
"""
from pathlib import Path
import hashlib
import json
import pickle
import joblib
import pandas as pd
import numpy as np

from dashboard.data import ROOT, RESULTS, RESEARCH


def main():
    destination = RESULTS / "dashboard"
    destination.mkdir(exist_ok=True)
    print("Reading fitted patient-level models", flush=True)
    state = joblib.load(RESEARCH / "prepared.joblib")
    benchmark = joblib.load(RESEARCH / "benchmarks.joblib")
    bundle = dict(preprocessor=state["pp"], imputer=state["imp"], scaler=state["scaler"],
                  models={k: benchmark["models"][f"domains:kmeans:{k}"] for k in [2, 3]},
                  model_names={k: f"domains:kmeans:{k}" for k in [2, 3]})
    for k, model in bundle["models"].items():
        predicted = model.predict(state["D"])
        np.testing.assert_array_equal(predicted, benchmark["assign"][f"domains:kmeans:{k}"])
    joblib.dump(bundle, destination / "profile_model.joblib")
    rows = []
    validation = state["test"]
    labels = benchmark["assign"]["domains:kmeans:3"][validation]
    for group in np.unique(labels):
        mask = labels == group
        for j, domain in enumerate(state["pp"].domains):
            rows.append(dict(model="domains:kmeans:3", cluster=int(group), domain=domain,
                             n=int(mask.sum()), mean=float(state["domains"][validation][mask, j].mean())))
    pd.DataFrame(rows).to_csv(destination / "robust_profiles.csv", index=False)

    print("Preparing aggregate clinical-unit tables", flush=True)
    with (RESULTS / "shared_infrastructure.pkl").open("rb") as stream:
        infra = pickle.load(stream)
    with (RESULTS / "eda_output.pkl").open("rb") as stream:
        eligible = pickle.load(stream)["df_eligible"]
    assert eligible.index.is_unique
    assert eligible.index.tolist() == infra["domain_score_index"]
    units = pd.read_excel(ROOT / "data" / "0_UNITATM.xlsx")
    frame = eligible[["C_UNITATMEDICA"]].copy()
    frame["cluster"] = infra["cluster_labels"]["MICE"]
    frame = frame.loc[(frame.C_UNITATMEDICA != 0) & (frame.cluster >= 0)].merge(
        units, left_on="C_UNITATMEDICA", right_on="C_UNITATM", how="left", validate="many_to_one")
    for column, name in [("N_UNITATM", "clinical_units"), ("N_GRUP", "diagnosis_groups")]:
        pd.crosstab(frame.cluster, frame[column]).to_csv(destination / (name + ".csv"))
    sources = [RESEARCH / "prepared.joblib", RESEARCH / "benchmarks.joblib",
               RESULTS / "shared_infrastructure.pkl", RESULTS / "eda_output.pkl", ROOT / "data/0_UNITATM.xlsx"]
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    (destination / "source_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Dashboard assets ready; saved assignments match both fitted models.", flush=True)


if __name__ == "__main__":
    main()
