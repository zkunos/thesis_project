"""Transparent ensemble implementations; not a verbatim port of author software."""
import numpy as np
from scipy.special import xlogy
from sklearn.metrics import normalized_mutual_info_score


def greedy_nmi(partitions,k,seed=42,max_iter=20):
    """Coordinate ascent of mean arithmetic-normalized MI with input partitions."""
    partitions=np.asarray(partitions,int);B,n=partitions.shape
    scores=[np.mean([normalized_mutual_info_score(a,b) for b in partitions]) for a in partitions]
    labels=partitions[int(np.argmax(scores))].copy()
    base=np.array([np.bincount(a,minlength=k) for a in partitions])
    counts=np.bincount(labels,minlength=k)
    tables=np.zeros((B,k,k),int)
    for j,p in enumerate(partitions):np.add.at(tables[j],(labels,p),1)
    xlog=lambda x:xlogy(x,x)
    baseS=xlog(base).sum(axis=1);Hbase=np.log(n)-baseS/n
    jointS=xlog(tables).sum(axis=(1,2));consS=xlog(counts).sum()
    def objective(joint,cons):
        H=np.log(n)-cons/n;I=(joint-cons-baseS)/n+np.log(n)
        return np.mean(2*I/np.maximum(H+Hbase,1e-15))
    obj=objective(jointS,consS);rng=np.random.default_rng(seed);indices=np.arange(B)
    for iteration in range(max_iter):
        moves=0
        for i in rng.permutation(n):
            a=labels[i]
            if counts[a]<=1:continue
            b=partitions[:,i];old=tables[indices,a,b]
            best=obj;chosen=None
            for c in range(k):
                if c==a:continue
                dest=tables[indices,c,b]
                deltaJ=xlog(old-1)-xlog(old)+xlog(dest+1)-xlog(dest)
                deltaC=xlog(counts[a]-1)-xlog(counts[a])+xlog(counts[c]+1)-xlog(counts[c])
                value=objective(jointS+deltaJ,consS+deltaC)
                if value>best+1e-10:best=value;chosen=(c,deltaJ,deltaC)
            if chosen is not None:
                c,deltaJ,deltaC=chosen
                tables[indices,a,b]-=1;tables[indices,c,b]+=1
                counts[a]-=1;counts[c]+=1;labels[i]=c
                jointS+=deltaJ;consS+=deltaC;obj=best;moves+=1
        if moves==0:break
    return labels,float(obj)
