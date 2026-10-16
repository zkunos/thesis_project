"""Render readable vector figures from the executed patient-level experiment.

Run from repository root with .venv-research/Scripts/python.exe.
The fixed k=3 fit reproduces the report's descriptive comparison; no model
selection or clinical analysis is changed by this presentation script.
"""
from pathlib import Path
import sys
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from threadpoolctl import threadpool_limits

out=ROOT/'results/research_2026';figs=ROOT/'report/Figures'
audit=pd.read_csv(out/'scaling_audit.csv')
common=pd.read_csv(out/'common_geometry_comparison.csv').iloc[0]
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                    'legend.fontsize':8.5,'pdf.fonttype':42})
labels=['Orientation','Attention','Visuo-\nperception','Language','Memory','Executive\nfunction']
colors=['#176B87','#E9803C','#668B49']
fig,axes=plt.subplots(2,1,figsize=(6,6),layout='constrained')
axes[0].bar(np.arange(6),audit.robust_scaled_variance,color=colors[0])
axes[0].axhline(1,color=colors[1],ls='--',label='Equal-domain variance = 1')
axes[0].set_xticks(np.arange(6),labels);axes[0].set_ylabel('Discovery variance')
axes[0].set_title('Domain weighting after robust scaling',fontsize=11);axes[0].legend()
v=np.array([[common.robust_k3_silhouette_robust,common.robust_k3_silhouette_equal_domain],
            [common.equal_k3_silhouette_robust,common.equal_k3_silhouette_equal_domain]])
x=np.arange(2)
axes[1].bar(x-.17,v[:,0],.34,label='Scored in robust space',color=colors[0])
axes[1].bar(x+.17,v[:,1],.34,label='Scored in equal-domain space',color=colors[1])
axes[1].set_xticks(x,['Robust k=3 labels','Equal-domain k=3 labels'])
axes[1].set_ylabel('Validation silhouette');axes[1].set_ylim(0,.8)
axes[1].set_title('The same partitions in both geometries',fontsize=11);axes[1].legend()
fig.savefig(figs/'extension_scaling_thesis.pdf');plt.close(fig)

state=joblib.load(out/'prepared.joblib');profiles=pd.read_csv(out/'scaling_profiles.csv')
with threadpool_limits(1):
    labs=KMeans(3,n_init=20,random_state=20261015).fit(state['D'][state['train']]).predict(state['D'][state['test']])
assert sorted(np.bincount(labs).tolist())==[51,185,1221]
fig,axes=plt.subplots(2,1,figsize=(6,6.4),sharex=True,sharey=True,layout='constrained')
for c in range(3):
    mask=labs==c
    axes[0].plot(np.arange(6),state['domains'][state['test']][mask].mean(axis=0),marker='o',
                 color=colors[c],label=f'Group {c+1} (n={mask.sum()})')
for c,g in profiles[profiles.model=='equal_domain:kmeans:3'].groupby('cluster'):
    g=g.set_index('domain').loc[list(audit.domain)]
    axes[1].plot(np.arange(6),g['mean'],marker='o',color=colors[c],label=f'Group {c+1} (n={int(g.n.iloc[0])})')
for ax,title in zip(axes,['Robust-scaled k-means, k=3','Equal-domain k-means, k=3']):
    ax.set_title(title,fontsize=11);ax.axhline(0,color='grey',lw=.6)
    ax.set_ylabel('Mean domain composite');ax.legend(loc='lower left',ncol=1)
    ax.set_ylim(-3.5,1)
axes[1].set_xticks(np.arange(6),labels)
fig.savefig(figs/'extension_profiles_thesis.pdf');plt.close(fig)
print('Rendered two vector figures for the thesis.')
