"""Render the saved MICE partition consistently in both assessment projections.

No embedding or clustering is refitted. The figure uses all saved assessments.
"""
from pathlib import Path
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
with (ROOT / "results/shared_infrastructure.pkl").open("rb") as stream:
    saved = pickle.load(stream)
labels = np.asarray(saved["cluster_labels"]["MICE"])
names = pd.read_csv(ROOT / "results/Cluster_Names.csv").set_index("cluster_id").clinical_name
colors = {0: "#2E8B7E", 1: "#C55B59", 2: "#D29A4D"}
assert set(np.unique(labels)) == set(names.index) == set(colors)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
for ax, coordinates, title, prefix in zip(axes,
        [saved["tsne_2d"], saved["umap_embeddings"]["MICE"]],
        ["MICE t-SNE projection", "MICE UMAP (first two coordinates)"], ["t-SNE", "UMAP"]):
    coordinates = np.asarray(coordinates)
    assert len(coordinates) == len(labels)
    for group in [0, 2, 1]:
        subset = coordinates[labels == group]
        ax.scatter(subset[:, 0], subset[:, 1], s=2, alpha=.45,
                   color=colors[group], linewidths=0, label=f"{names[group]} (n={(labels == group).sum():,})")
    ax.set(title=title, xlabel=f"{prefix} 1", ylabel=f"{prefix} 2")
    ax.grid(alpha=.12)
handles, legend_labels = axes[0].get_legend_handles_labels()
fig.legend(handles, legend_labels, loc="lower center", ncol=3, frameon=False, markerscale=4)
fig.subplots_adjust(left=.09, right=.99, top=.9, bottom=.2, wspace=.26)
fig.savefig(ROOT / "report/Figures/tsne_umap_clusters.png", dpi=200)
plt.close(fig)
print(f"Rendered {len(labels):,} saved MICE assignments in three groups.")
