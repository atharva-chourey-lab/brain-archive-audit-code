"""AQUATIC THREAD — Phase 3 analysis (EXPLORATORY / post-hoc throughout).

Inputs: aquatic/measurements_aquatic_raw.json (Phase 2, project pipeline),
outputs/cross_species_volumes_v3.csv (the land set + registered-line table).

Outputs:
  aquatic/measurements_aquatic.csv  — v3 column style, aquatic species only.
  aquatic/residuals_exploratory.csv — every aquatic residual computed anywhere
      in this thread, each tagged with its method class. MRI-label residuals
      (none exist — see report) and LITERATURE residuals are never pooled.

The registered line (PREDICTION.md, fit on MRI catalogue labels only):
  log10(hippocampus_cm3) = -1.6609 + 0.8467 * log10(brain_cm3)
It is applied to literature brain volumes ONLY as a labelled cross-method
exercise, mirroring the project's blind-benchmark design (BENCHMARK.md).
"""
import json, numpy as np, pandas as pd

A, B = -1.6609, 0.8467  # registered line: intercept, slope

def predict(brain_cm3):
    return float(10 ** (A + B * np.log10(brain_cm3)))

def resid(measured, brain_cm3):
    p = predict(brain_cm3)
    return p, 100.0 * (measured - p) / p

raw = json.load(open("aquatic/measurements_aquatic_raw.json"))
v3 = pd.read_csv("outputs/cross_species_volumes_v3.csv").set_index("species")

# QC verdicts from Phase 2 forensics (see REPORT_aquatic.md for the evidence).
# denominator_valid: can brain_vol_cm3 be used as a whole-brain denominator?
QC = {
    "Bottlenose_dolphin": {
        "denominator_valid": True,
        "qc": "Atlas mask and Otsu mask agree (515.5 vs 492.9); hippocampus "
              "file empty; 'cerebellum' label is a sparse fragment (about 2% "
              "fill of its bounding box) in the correct posterior position - "
              "not a whole-cerebellum volume; corpus callosum nz=900 junk"},
    "La_Plata_dolphin": {
        "denominator_valid": False,
        "qc": "Otsu mask is 99.999% telencephalon voxels (mask minus label = "
              "62 voxels): the pipeline's 'brain' IS the telencephalon on "
              "this scan, so the whole-brain denominator FAILED; telencephalon "
              "label itself is one coherent component (99.97%)"},
    "Platypus": {
        "denominator_valid": False,
        "qc": "Otsu mask covers the whole head (bill, muscle, skull), not "
              "the brain: 73.91 cm3 vs literature whole-brain 8.85 cm3; the "
              "telencephalon label alone (13.38) also exceeds the literature "
              "whole brain - specimen's catalogue numbers irreconcilable "
              "with the species' known brain size; label stored at value 255"},
    "Nile_crocodile": {
        "denominator_valid": False,
        "qc": "MRI header magic/datatype zeroed (repaired in memory only); "
              "Otsu mask is 99.85% telencephalon voxels - whole-brain "
              "denominator FAILED as for La Plata; telencephalon label "
              "coherent (values 255/254)"},
    "Nursehound": {
        "denominator_valid": False,
        "qc": "whole-specimen scan; Otsu mask sprawls over muscle/cartilage "
              "(73.68 cm3 is not a brain volume); telencephalon label is a "
              "single coherent component, 100% inside the mask"},
}

# ---------------------------------------------------------------- aquatic CSV
rows = []
for sp, rec in raw.items():
    if sp.startswith("_"):
        continue
    f = rec["files"]
    row = {"species": sp}
    # brain denominator, v2 rule: catalogue Atlas mask first, else Otsu
    if "Atlas" in f and f["Atlas"]["nz"] > 1000:
        row["brain_vol_cm3"] = f["Atlas"]["vol_cm3_own_zooms"]
        row["brain_vol_source"] = "catalogue_atlas_mask"
        row["atlas_mask_cm3"] = f["Atlas"]["vol_cm3_own_zooms"]
    else:
        row["brain_vol_cm3"] = rec["mri"]["otsu_brain_cm3"]
        row["brain_vol_source"] = "otsu_mask"
    for key, col in [("Telencephalon", "telencephalon_cm3"),
                     ("Cerebellum", "cerebellum_cm3"),
                     ("Cerebrum", "cerebrum_cm3"),
                     ("Striatum", "striatum_cm3"),
                     ("Neocortex", "neocortex_cm3")]:
        if key in f:
            if f[key]["nz"] > 1000:
                row[col] = f[key]["vol_cm3_own_zooms"]
            else:
                row[col.replace("_cm3", "_note")] = \
                    f"empty/placeholder (nz={f[key]['nz']})"
    if "Hippocampus" in f:
        h = f["Hippocampus"]
        if h["nz"] > 1000:
            row["hippocampus_cm3"] = h["vol_cm3_own_zooms"]
            row["data_class"] = "catalogue_label"
        else:
            row["hippocampus_note"] = f"empty/placeholder (nz={h['nz']})"
            row["data_class"] = "none"
    else:
        row["hippocampus_note"] = "no Hippocampus file in catalogue folder"
        row["data_class"] = "none"
    if "Corpus_callosum" in f and f["Corpus_callosum"]["nz"] <= 1000:
        row["corpus_callosum_note"] = \
            f"empty/placeholder (nz={f['Corpus_callosum']['nz']})"
    if pd.notna(row.get("hippocampus_cm3")) and pd.notna(row.get("brain_vol_cm3")):
        row["hippocampus_pct"] = round(
            100 * row["hippocampus_cm3"] / row["brain_vol_cm3"], 4)
        p, dev = resid(row["hippocampus_cm3"], row["brain_vol_cm3"])
        row["predicted_hippocampus_cm3"] = round(p, 4)
        row["deviation_pct"] = round(dev, 1)
    row["qc"] = QC[sp]["qc"]
    if not QC[sp]["denominator_valid"]:
        # the mask number stays on record, but it is not a whole brain:
        # no share may be computed against it
        row["brain_vol_source"] += " [QC FAIL: not a whole-brain mask - see qc]"
    if (QC[sp]["denominator_valid"]
            and pd.notna(row.get("telencephalon_cm3"))
            and pd.notna(row.get("brain_vol_cm3"))):
        row["telencephalon_pct"] = round(
            100 * row["telencephalon_cm3"] / row["brain_vol_cm3"], 2)
    rows.append(row)
aq = pd.DataFrame(rows)
cols = [c for c in ["species", "telencephalon_cm3", "telencephalon_pct",
                    "hippocampus_note", "striatum_note", "brain_vol_source",
                    "hippocampus_cm3", "atlas_mask_cm3", "cerebellum_cm3",
                    "corpus_callosum_note", "striatum_cm3", "cerebrum_cm3",
                    "neocortex_cm3", "brain_vol_cm3", "hippocampus_pct", "qc",
                    "data_class", "predicted_hippocampus_cm3", "deviation_pct"]
        if c in aq]
aq[cols].to_csv("aquatic/measurements_aquatic.csv", index=False)
print("== measurements_aquatic.csv")
print(aq[cols].to_string(index=False))

# ------------------------------------------------- telencephalon shares, land
land = v3.dropna(subset=["telencephalon_cm3", "brain_vol_cm3"]).copy()
land["tel_share"] = 100 * land["telencephalon_cm3"] / land["brain_vol_cm3"]
print("\n== telencephalon share of brain (%)")
print("LAND (catalogue, n=%d): median %.1f, range %.1f-%.1f"
      % (len(land), land["tel_share"].median(),
         land["tel_share"].min(), land["tel_share"].max()))
for _, r in aq.iterrows():
    if pd.notna(r.get("telencephalon_pct")):
        print(f"AQUATIC {r['species']:20s} {r['telencephalon_pct']:6.1f} "
              f"(brain {r['brain_vol_cm3']} cm3, {r['brain_vol_source']})")
print("land by species:", {k: round(v, 1) for k, v in
                           land["tel_share"].sort_values().items()})

# ------------------------------------------------------- literature residuals
# Patzke et al. 2015, Brain Struct Funct 220:361-383, Table 1 (Vb = Mb/1.036).
# S codes: 1 Pirlot & Nelson 1978; 3 Reep et al. 2007; 4 Montie et al. 2008
# (MRI volumetry); 5 Patzke et al. current study (histology/stereology).
LIT = [
    ("Tursiops truncatus (bottlenose dolphin)", 1476.83, 1.05,
     "literature_histology", "Patzke et al. 2015 Table 1, S=5"),
    ("Phocoena phocoena (harbour porpoise)", 477.32, 0.60,
     "literature_histology", "Patzke et al. 2015 Table 1, S=5 (2 specimens, mean Vb)"),
    ("Lagenorhynchus acutus (Atlantic white-sided dolphin)", 1267.57, 1.73,
     "literature_MRI", "Patzke et al. 2015 Table 1, S=4 = Montie et al. 2008 MRI (3 specimens, means)"),
    ("Balaenoptera acutorostrata (minke whale)", 2750.97, 1.425,
     "literature_histology", "Patzke et al. 2015 Table 1, S=5 (2 specimens, means)"),
    ("Ornithorhynchus anatinus (platypus)", 8.85, 0.51,
     "literature_histology", "Patzke et al. 2015 Table 1, S=1 = Pirlot & Nelson 1978"),
    ("Trichechus manatus (manatee; NOT in catalogue — aquatic control)", 337.84, 3.63,
     "literature_histology", "Patzke et al. 2015 Table 1, S=3 = Reep et al. 2007"),
    ("Hippopotamus amphibius (hippo, specimen 1; NOT in catalogue — semi-aquatic, cetacean sister group)", 559.27, 6.81,
     "literature_histology", "Patzke et al. 2015 Table 1, S=5"),
    ("Hippopotamus amphibius (hippo, specimen 2; NOT in catalogue — semi-aquatic, cetacean sister group)", 393.34, 3.63,
     "literature_histology", "Patzke et al. 2015 Table 1, S=5"),
]
print("\n== literature residuals vs the registered MRI-label line "
      "(EXPLORATORY, cross-method, never pooled with MRI-label residuals)")
out = []
for name, vb, vh, cls, src in LIT:
    p, dev = resid(vh, vb)
    row = {"species": name, "brain_cm3_lit": vb, "hippocampus_cm3_lit": vh,
           "predicted_cm3_registered_line": round(p, 3),
           "residual_pct": round(dev, 1), "method_class": cls, "source": src}
    if cls == "literature_histology":
        # Two Rulers: histology runs ~1.3-1.6x MRI. Deflating the histology
        # value to an MRI-equivalent makes a BELOW-line residual more
        # negative, an ABOVE-line residual smaller. Range, not a point.
        for f in (1.3, 1.6):
            _, d = resid(vh / f, vb)
            row[f"residual_pct_if_deflated_{f}x"] = round(d, 1)
    out.append(row)
    print(f"{name:58s} Vb={vb:8.2f} Vh={vh:6.3f} pred={p:7.3f} "
          f"residual={dev:+7.1f}%  [{cls}]")
pd.DataFrame(out).to_csv("aquatic/residuals_exploratory.csv", index=False)
print("\nwrote aquatic/measurements_aquatic.csv + residuals_exploratory.csv")
