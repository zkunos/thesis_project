"""Read trusted, local analysis outputs without refitting the experiments."""
from functools import lru_cache
from pathlib import Path
import json
import pickle

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESEARCH = RESULTS / "research_2026"
DOMAINS = ["Orientation", "Attention", "Visuoperception", "Language", "Memory", "Executive Function"]
COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#555555", "#8C564B"]
REPRESENTATIONS = {"domains": "Robust domains", "residual": "PC1 residuals",
                   "tests": "14 tests", "without_orientation": "Without orientation"}
METHODS = {"kmeans": "K-means", "pam": "Sampled PAM", "gmm_full": "Full Gaussian mixture",
           "gmm_tied": "Tied Gaussian mixture", "hdbscan": "HDBSCAN", "umap_hdbscan": "UMAP + HDBSCAN"}


@lru_cache(maxsize=40)
def table(name, research=False, index_col=None):
    return pd.read_csv((RESEARCH if research else RESULTS) / name, index_col=index_col)


@lru_cache(maxsize=16)
def saved(name):
    # Only application-selected files from the local analysis directory are used.
    with (RESULTS / (name + ".pkl")).open("rb") as stream:
        return pickle.load(stream)


@lru_cache(maxsize=4)
def metadata(name="run_manifest.json"):
    return json.loads((RESEARCH / name).read_text(encoding="utf-8"))


def legacy_profiles(method="MICE"):
    infra = saved("shared_infrastructure")
    return pd.DataFrame(infra["domain_scores"][method], columns=infra["domain_score_columns"])


def cohort_z(frame):
    scale = frame.std(ddof=0).replace(0, 1)
    return (frame - frame.mean()) / scale


def names(method="MICE"):
    if method == "MICE":
        return {int(r.cluster_id): f"{int(r.cluster_id)} · {r.clinical_name}"
                for r in table("Cluster_Names.csv").itertuples()}
    labels = saved("shared_infrastructure")["cluster_labels"][method]
    return {int(k): f"Group {int(k)}" for k in np.unique(labels) if k >= 0}


def hypothesis_rows():
    h2, h3, h4 = (saved(f"h{i}_results") for i in [2, 3, 4])
    return [
        ("H1 · Stability and discreteness", "Partially supported",
         "Embedding separation passes the selected thresholds; moderate resampling agreement and variable group counts leave discreteness unresolved."),
        ("H2 · Imputation robustness", "Supported within a fixed rule",
         f"Mean ARI {h2['mean_ari']:.3f}. The same MICE-fitted transformation and three-group partition are applied across imputations."),
        ("H3 · Clinical-unit association", "Association supported",
         f"Cramér's V {h3['cramers_v']:.3f}. Patient-grouped validation does not show clear added predictive value beyond diagnosis."),
        ("H4 · Domain aggregation", "Conditioning improves",
         f"Mean VIF falls from {h4['variable_vif']:.2f} to {h4['domain_vif']:.2f}; silhouette changes only from {h4['variable_silhouette']:.3f} to {h4['domain_silhouette']:.3f}.")]


def research_summary():
    manifest = metadata()
    agreement = table("refit_agreement.csv", True)
    imputation = agreement[(agreement.source == "imputation_draw") & (agreement.method == "kmeans")].set_index("k")
    geometry = table("common_geometry_comparison.csv", True).iloc[0]
    trajectory = table("trajectory_model_comparison.csv", True)
    viable = trajectory[trajectory.converged & (trajectory.minimum_train_class_fraction >= .05)]
    selected = viable.loc[viable.bic.idxmin()]
    return dict(discovery=manifest["train_patients"], validation=manifest["validation_patients"],
                ari2=float(imputation.loc[2, "mean_ari"]), ari3=float(imputation.loc[3, "mean_ari"]),
                scaling_ari=float(geometry.ari_robust_vs_equal),
                trajectory_n=int(selected.n_train + selected.n_validation), trajectory_k=int(selected.k))


@lru_cache(maxsize=1)
def profile_model():
    import joblib
    return joblib.load(RESULTS / "dashboard" / "profile_model.joblib")


def assign_profile(values, groups=2):
    """Apply saved discovery transformations; do not learn from user input."""
    bundle = profile_model()
    pp = bundle["preprocessor"]
    frame = pd.DataFrame([values]).reindex(columns=pp.columns_).astype(float)
    observed = frame.notna().to_numpy()[0]
    if not observed.any():
        raise ValueError("Enter at least one observed test score.")
    if np.isinf(frame.to_numpy()).any():
        raise ValueError("Scores must be finite numbers or blank.")
    transformed = pp.transform_tests(frame)
    completed = bundle["imputer"].transform(transformed)
    domains = pp.aggregate(completed)
    scaled = bundle["scaler"].transform(domains)
    model = bundle["models"][int(groups)]
    label = int(model.predict(scaled)[0])
    distances = model.transform(scaled)[0]
    clipped = observed & ((frame.to_numpy()[0] < pp.lo_) | (frame.to_numpy()[0] > pp.hi_))
    return dict(cluster=label, domains=domains[0], distances=distances,
                observed=int(observed.sum()), clipped=[c for c, flag in zip(pp.columns_, clipped) if flag],
                imputed=[c for c, flag in zip(pp.columns_, observed) if not flag],
                center=bundle["scaler"].inverse_transform(model.cluster_centers_[[label]])[0])
