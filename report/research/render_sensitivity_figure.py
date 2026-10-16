"""Render the saved variable-availability sensitivity without plotting failed fits as scores."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
data = pd.read_csv(ROOT / 'results/Sensitivity_Analysis.csv')
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
fig, axes = plt.subplots(1, 2, figsize=(10, 3.3), layout='constrained')
silhouette = data.silhouette.where(data.n_clusters >= 2, np.nan)
for ax, values, title, ylabel in zip(axes, [silhouette, data.noise_fraction],
        ['(c) Silhouette', '(d) Noise before reassignment'], ['Silhouette', 'Noise fraction']):
    ax.plot(data.threshold, values, 'o-', color='#0072B2')
    ax.axvline(50, color='#8A8F98', linestyle='--', linewidth=1)
    ax.set(title=title, xlabel='Maximum variable missingness (%)', ylabel=ylabel,
           xlim=(28, 72), xticks=data.threshold)
    ax.grid(alpha=.15)
axes[0].annotate('No clusters', (30, .4), xytext=(30,.445), ha='left', fontsize=10,
                 arrowprops={'arrowstyle':'-', 'color':'#8A8F98'})
fig.savefig(ROOT/'report/Figures/sensitivity_analysis_b.png',dpi=200)
plt.close(fig)
