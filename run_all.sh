#!/usr/bin/env bash
# Re-execute the full pipeline of analysis notebooks in dependency order.
# Each notebook is executed in place via nbconvert and written to N_executed.ipynb.
# Stops on first failure.
set -euo pipefail

cd "$(dirname "$0")/notebooks"

NB_LIST=(
    "0_EDA_Missingness.ipynb"
    "1_Missingness_Strategy.ipynb"
    "2_Deep_Learning_Imputation.ipynb"
    "3_Clustering_Analysis.ipynb"
    "4_Paper_Clustering_Comparison.ipynb"
    "5_Improved_Clustering_Infrastructure.ipynb"
    "6_H1_Stability.ipynb"
    "7_H2_Imputation_Robustness.ipynb"
    "8_H3_Clinical_Unit_Association.ipynb"
    "9_H4_Domain_vs_Variable_Level.ipynb"
    "10_Synthesis_Final_Report.ipynb"
    "11_Feature_Importance.ipynb"
    "12_Cross_Validation_Stability.ipynb"
    "13_Sensitivity_Analysis.ipynb"
    "14_Backlog_Additions.ipynb"
    "14b_Fix_A2_Parametric_pvalues.ipynb"
)

START=$(date +%s)
for NB in "${NB_LIST[@]}"; do
    BASE="${NB%.ipynb}"
    # NB index = leading numeric prefix (handles 14b)
    NUM="${BASE%%_*}"
    OUT="${NUM}_executed.ipynb"
    echo "=== $(date +%H:%M:%S)  running $NB -> $OUT ==="
    jupyter nbconvert --to notebook --execute "$NB" \
        --output "$OUT" --ExecutePreprocessor.timeout=3600
done
END=$(date +%s)
echo "=== DONE in $((END - START))s ==="
