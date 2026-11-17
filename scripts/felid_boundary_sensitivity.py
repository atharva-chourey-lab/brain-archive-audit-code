"""FELID RECONCILIATION — TEST B (PREDICTION.md §4): boundary sensitivity of the
catalogue labels. Method-independent bound on the delineation hypothesis: dilate
each catalogue Hippocampus label by 1 and 2 voxels (scipy binary_dilation,
default 6-connectivity), constrained to the telencephalon/brain mask (lion: its
Telencephalon label; leopard: its Atlas mask), and measure at native zooms.
If even a 2-voxel-more-generous pen cannot approach the Reep values, tight
delineation alone cannot explain the gap. Prints the combined table with the
pre-registered gap-closure grading (closure = (new - catalogue)/(Reep -
catalogue); >=50% delineation main driver, <20% labels exonerated, else mixed),
reading Test A volumes from outputs/felid_reconciliation_testA.csv if present.
"""
import nibabel as nib, numpy as np, csv, os
from scipy.ndimage import binary_dilation

CASES = [
    ("Lion", "data/lion/atlas/Hippocampus.nii.gz", "data/lion/atlas/Telencephalon.nii.gz", 2.022, 4.496),
    ("Leopard", "data/brain_catalogue_full/Leopard/Hippocampus.nii.gz", "data/brain_catalogue_full/Leopard/Atlas.nii.gz", 1.178, 3.121),
]
testA = {}
if os.path.exists("outputs/felid_reconciliation_testA.csv"):
    for r in csv.DictReader(open("outputs/felid_reconciliation_testA.csv")):
        testA[r["species"]] = float(r["volume_cm3"])

def grade(closure):
    return ">=50%: delineation main driver" if closure >= 0.50 else ("<20%: labels exonerated" if closure < 0.20 else "20-50%: mixed")

# Test A QC outcome (checked 2026-11-17): BOTH propagations FAILED placement QC —
# Dice vs the catalogue labels 0.000 (lion) / 0.001 (leopard), centroid offsets
# 33.2 / 15.9 mm. Their volumes measure the wrong territory, so Test A grades
# VOID regardless of the arithmetic closure; Test B carries the verdict.
TESTA_VOID = {"Lion", "Leopard"}

rows = []
print(f"{'species':<9} {'catalogue':>9} {'+1vox':>8} {'+2vox':>8} {'D99form':>8} {'Reep':>7} | closures: +1 / +2 / TestA")
for sp, lab_p, mask_p, cat, reep in CASES:
    lim = nib.load(lab_p); lab = np.squeeze(np.asanyarray(lim.dataobj)) > 0
    con = np.squeeze(np.asanyarray(nib.load(mask_p).dataobj)) > 0
    assert lab.shape == con.shape
    vox = float(np.prod(lim.header.get_zooms()[:3])) / 1000.0
    v0 = float(lab.sum()) * vox
    assert abs(v0 - cat) < 0.01, f"{sp} catalogue volume check failed: {v0} vs {cat}"
    out = {}
    for k in (1, 2):
        dil = binary_dilation(lab, iterations=k) & con
        out[k] = float(dil.sum()) * vox
    a = testA.get(sp)
    clos = lambda v: (v - cat) / (reep - cat)
    print(f"{sp:<9} {cat:>9.3f} {out[1]:>8.3f} {out[2]:>8.3f} {a if a else float('nan'):>8.3f} {reep:>7.3f} | "
          f"{clos(out[1])*100:5.1f}% / {clos(out[2])*100:5.1f}% / {(clos(a)*100 if a else float('nan')):5.1f}%")
    rows.append(dict(species=sp, catalogue_cm3=cat, plus1vox_cm3=round(out[1], 3), plus2vox_cm3=round(out[2], 3),
                     testA_propagated_cm3=a, reep_cm3=reep,
                     closure_plus1_pct=round(clos(out[1]) * 100, 1), closure_plus2_pct=round(clos(out[2]) * 100, 1),
                     closure_testA_pct=(round(clos(a) * 100, 1) if a else None),
                     grade_testB=grade(clos(out[2])),
                     grade_testA=("VOID - propagation failed placement QC (Dice ~0)" if sp in TESTA_VOID else (grade(clos(a)) if a else None))))
with open("outputs/felid_reconciliation_testB.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("wrote outputs/felid_reconciliation_testB.csv")
for r in rows:
    print(f"{r['species']}: Test B grade (at +2 vox): {r['grade_testB']} | Test A grade: {r['grade_testA']}")
