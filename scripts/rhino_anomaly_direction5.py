#!/usr/bin/env python3
"""Rhino anomaly investigation — Direction 5 (line-side robustness) and the
Direction 2 MRI-class share table.

Pre-registered in PREREGISTRATION_rhino_anomaly_2026-11-17.md (commit e53edfd)
BEFORE this script was run. No refitting of the registered line; the
leave-one-out refit is a declared exploratory sensitivity only.
"""
import json
import math

import numpy as np
import pandas as pd

# ---------------------------------------------------------------- registered
# Registered line (PREDICTION.md s.1), fixed ruler, never refitted.
REG_A, REG_B = -1.6609, 0.8467


def reg_pred(vb):
    return 10 ** (REG_A + REG_B * math.log10(vb))


def patzke_pred(vb):
    # Patzke et al. 2015 exponential, as published / as in scripts/benchmark.py:
    # ln(Vh) = 9.26 * (0.72 - exp(-0.097 * ln(Vb)))
    return math.exp(9.26 * (0.72 - math.exp(-0.097 * math.log(vb))))


FIT_SET = {  # PREDICTION.md s.1 fit set (catalogue labels only)
    "Black_rhinoceros", "Cat", "Cheetah", "Ferret", "Giant_panda",
    "Leopard", "Lion", "Red_kangaroo",
}
ARTIFACT = {"Sloth_bear", "Giraffe"}  # one-sided / unilateral labels

v3 = pd.read_csv("outputs/cross_species_volumes_v3.csv")
pts = v3.dropna(subset=["hippocampus_cm3"]).copy()
assert len(pts) == 14, len(pts)

rows = []
for _, r in pts.iterrows():
    sp, vb, vh = r["species"], float(r["brain_vol_cm3"]), float(r["hippocampus_cm3"])
    cls = r["data_class"]
    kind = ("fit_member" if sp in FIT_SET else
            "artifact_flagged_label" if sp in ARTIFACT else
            "label_not_in_fit" if cls == "catalogue_label" else
            "model_estimated")
    rows.append({
        "species": sp, "brain_cm3": vb, "hippocampus_cm3": vh,
        "share_pct": 100.0 * vh / vb, "data_class": cls, "kind": kind,
        "reg_pred": reg_pred(vb),
        "resid_reg_pct": 100.0 * (vh - reg_pred(vb)) / reg_pred(vb),
        "patzke_pred": patzke_pred(vb),
        "resid_patzke_pct": 100.0 * (vh - patzke_pred(vb)) / patzke_pred(vb),
    })
tab = pd.DataFrame(rows)

out = {}

# ------------------------------------------------- verify fit-set transcription
fit = tab[tab["species"].isin(FIT_SET)]
x = np.log10(fit["brain_cm3"].values)
y = np.log10(fit["hippocampus_cm3"].values)
b, a = np.polyfit(x, y, 1)
out["fitset_check"] = {
    "slope_refit": round(float(b), 4), "intercept_refit": round(float(a), 4),
    "registered_slope": REG_B, "registered_intercept": REG_A,
    "r": round(float(np.corrcoef(x, y)[0, 1]), 3),
}

# ------------------------------------------------------- rhino vs Patzke model
rh = tab[tab["species"] == "Black_rhinoceros"].iloc[0]
out["rhino_vs_patzke_model"] = {
    "at_Vb_442.65": {
        "patzke_pred": round(patzke_pred(442.65), 3),
        "label_6.854_resid_pct": round(100 * (6.854 - patzke_pred(442.65)) / patzke_pred(442.65), 1),
        "tracing_6.97_resid_pct": round(100 * (6.97 - patzke_pred(442.65)) / patzke_pred(442.65), 1),
    },
    "compilation_row_at_Vb_512.55": {
        "patzke_pred": round(patzke_pred(512.55), 3),
        "observed_7.48_resid_pct": round(100 * (7.48 - patzke_pred(512.55)) / patzke_pred(512.55), 1),
    },
    "bhagwandin_4.71_at_Vb_512.55_resid_pct":
        round(100 * (4.71 - patzke_pred(512.55)) / patzke_pred(512.55), 1),
}

# ------------------------------------------------- leave-one-out (exploratory)
loo = fit[fit["species"] != "Black_rhinoceros"]
xb, yb = np.log10(loo["brain_cm3"].values), np.log10(loo["hippocampus_cm3"].values)
b2, a2 = np.polyfit(xb, yb, 1)
loo_pred = 10 ** (a2 + b2 * math.log10(442.65))
out["loo_sensitivity_EXPLORATORY"] = {
    "n": int(len(loo)), "slope": round(float(b2), 4), "intercept": round(float(a2), 4),
    "r": round(float(np.corrcoef(xb, yb)[0, 1]), 3),
    "pred_at_442.65": round(float(loo_pred), 3),
    "label_resid_pct": round(100 * (6.854 - loo_pred) / loo_pred, 1),
    "tracing_resid_pct": round(100 * (6.97 - loo_pred) / loo_pred, 1),
}

# --------------------------------------------------------------------- ranks
direct = tab[tab["data_class"] == "catalogue_label"].copy()
direct_sorted = direct.sort_values("resid_reg_pct", ascending=False)
out["direct_label_resid_rank"] = [
    {"rank": i + 1, "species": r.species, "resid_reg_pct": round(r.resid_reg_pct, 1),
     "kind": r.kind}
    for i, r in enumerate(direct_sorted.itertuples())]
share_sorted = tab.sort_values("share_pct", ascending=False)
out["share_rank_all14"] = [
    {"rank": i + 1, "species": r.species, "share_pct": round(r.share_pct, 3),
     "data_class": r.data_class, "kind": r.kind}
    for i, r in enumerate(share_sorted.itertuples())]
large = direct[direct["brain_cm3"] > 100].sort_values("share_pct", ascending=False)
out["share_rank_large_brain_direct_labels"] = [
    {"rank": i + 1, "species": r.species, "share_pct": round(r.share_pct, 3),
     "brain_cm3": r.brain_cm3, "kind": r.kind}
    for i, r in enumerate(large.itertuples())]

tab_out = tab.sort_values("brain_cm3")
tab_out.to_csv("outputs/rhino_anomaly_mri_class_table.csv", index=False)
with open("outputs/rhino_anomaly_direction5.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
print("\nFull 14-point table written to outputs/rhino_anomaly_mri_class_table.csv")
