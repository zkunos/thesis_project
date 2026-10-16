"""Verify source alignment and create extract-scoped assessment identifiers."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from .preprocessing import FEATURES


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def load_verified(root, output):
    root, output = Path(root), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    source = root / 'data/0_tests2.xlsx'
    raw = pd.read_excel(source)
    previous = pd.read_csv(root / 'results/eligible_data_matrix.csv', index_col=0)
    assert previous.index.is_unique and previous.index.isin(raw.index).all()
    assert set(previous.columns) == set(FEATURES)
    assert np.allclose(previous.to_numpy(float), raw.loc[previous.index, previous.columns].to_numpy(float), equal_nan=True), 'Saved matrix no longer matches source'
    assert np.array_equal(previous.index, raw.index[raw[FEATURES].notna().any(axis=1)])
    df = raw.loc[previous.index].copy()
    assert df['ID'].notna().all() and df['TSI_TO_ASSESSMENT_DAYS'].notna().all()
    digest = sha256(source)
    df['source_row'] = df.index
    # No natural assessment ID is supplied. These identifiers are stable within
    # this exact extract, not transferable between different source versions.
    df['assessment_key'] = [f'{digest[:16]}:{i}' for i in df.index]
    df['patient_key'] = [hashlib.sha256(str(v).encode()).hexdigest()[:20] for v in df.ID]
    assert df.assessment_key.is_unique
    assert df.groupby('patient_key').ID.nunique().max() == 1
    df['observed_tests'] = df[FEATURES].notna().sum(axis=1)
    ordered = df.sort_values(['ID', 'TSI_TO_ASSESSMENT_DAYS', 'source_row'])
    index = ordered.drop_duplicates('ID').copy()
    counts = df.groupby('ID').size()
    df[['assessment_key','patient_key','source_row','observed_tests','TSI_TO_ASSESSMENT_DAYS']].to_csv(output / 'assessment_manifest.csv', index=False)
    visit_audit = df.groupby('ID').agg(n_visits=('ID','size'),
        first_day=('TSI_TO_ASSESSMENT_DAYS','min'), last_day=('TSI_TO_ASSESSMENT_DAYS','max'),
        n_unique_times=('TSI_TO_ASSESSMENT_DAYS','nunique'),
        n_injury_ages=('AGE_INJURY','nunique'), patient_key=('patient_key','first'))
    visit_audit['span_years'] = (visit_audit.last_day-visit_audit.first_day)/365.25
    visit_audit.drop(columns=[]).reset_index(drop=True).to_csv(output/'trajectory_data_audit.csv',index=False)
    audit = dict(source_sha256=digest, raw_rows=len(raw), eligible_rows=len(df),
        eligible_patients=int(df.ID.nunique()), index_rows=len(index), features=FEATURES,
        saved_matrix_matches=True, actual_row_rule='At least one observed retained test',
        at_least_half_observed=int((df.observed_tests >= 7).sum()),
        complete_rows=int(df[FEATURES].notna().all(axis=1).sum()),
        visits_per_patient={str(k):int(v) for k,v in counts.value_counts().sort_index().items()},
        duplicate_patient_times=int(df.duplicated(['ID','TSI_TO_ASSESSMENT_DAYS']).sum()),
        patients_multiple_injury_ages=int((visit_audit.n_injury_ages>1).sum()),
        index_missing_fraction=float(index[FEATURES].isna().to_numpy().mean()),
        index_at_least_half_observed=int((index.observed_tests>=7).sum()),
        assessment_key_scope='SHA256 of source file plus zero-based source row; no natural assessment ID available')
    (output/'data_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    return df, index, audit
