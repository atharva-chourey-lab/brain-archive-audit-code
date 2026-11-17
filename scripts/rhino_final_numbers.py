"""Rhino investigation — final numbers (post-hoc): thread/dust accounting,
per-side bulk volumes, conservative-core residuals, and Test-4 comparative
hippocampus shares (our MRI set + large-brained histology species from the
benchmark transcription). Prints everything for the report."""
import nibabel as nib, numpy as np, sys
from scipy import ndimage
sys.path.insert(0, "scripts")
from benchmark import REEP, PATZKE  # transcribed tables (import runs no main)

BASE = "data/brain_catalogue_full/Black_rhinoceros"
hipp = np.squeeze(np.asanyarray(nib.load(f"{BASE}/Hippocampus.nii.gz").dataobj)) > 0
vox = 0.45 ** 3 / 1000.0
LINE = lambda b: 10 ** (-1.6609 + 0.8467 * np.log10(b))
MEAS, BRAIN = 6.854, 442.65

print("--- label accounting ---")
bulk = hipp.copy(); bulk[:, :140, :] = False; bulk[:, 215:, :] = False
print(f"bulk slab ax1 140..214: {bulk.sum() * vox:.3f} cm3 ({100 * bulk.sum() / hipp.sum():.1f}% of label)")
print(f"anterior thread ax1 <140: {hipp[:, :140, :].sum() * vox:.3f} cm3 | posterior dust ax1 >=215: {hipp[:, 215:, :].sum() * vox:.3f} cm3")
left = hipp.copy(); left[134:, :, :] = False
right = hipp.copy(); right[:133, :, :] = False
print(f"per side (whole label): L {left.sum() * vox:.3f} cm3, R {right.sum() * vox:.3f} cm3")
lb, rb = bulk.copy(), bulk.copy(); lb[134:, :, :] = False; rb[:133, :, :] = False
print(f"per side (bulk only):   L {lb.sum() * vox:.3f} cm3, R {rb.sum() * vox:.3f} cm3")
for tag, v in (("top-2 components only", 6.780), ("smaller side x2", 2 * left.sum() * vox),
               ("1-vox erosion (extreme looseness bound)", 4.417), ("measured label", MEAS)):
    print(f"  {tag:<42} {v:.3f} cm3 -> residual vs line@442.65: {100 * (v - LINE(BRAIN)) / LINE(BRAIN):+.1f}%")

print("\n--- Test 4: hippocampus share of brain, large brains ---")
print("OUR MRI / catalogue-label set:")
for sp, h, b in (("Black rhinoceros (measured)", 6.854, 442.65),
                 ("Giraffe (bilateral-equivalent est.)", 5.83, 618.46),
                 ("Lion", 2.022, 188.08), ("Leopard", 1.178, 99.14),
                 ("Cheetah", 0.848, 67.93), ("Giant panda", 1.065, 181.71),
                 ("Red kangaroo", 0.200, 27.23), ("Ferret (small brain)", 0.173, 6.13)):
    print(f"  {sp:<38} share {100 * h / b:.3f}%  (line predicts {100 * LINE(b) / b:.3f}%)")
print("Histology record (benchmark transcription; shares run high vs MRI by method):")
seen = {}
for name, mb, vb, vh, src in PATZKE:
    if vb >= 300:
        seen.setdefault(name, []).append((vb, vh))
for name, rows in sorted(seen.items()):
    vb = np.mean([r[0] for r in rows]); vh = np.mean([r[1] for r in rows])
    print(f"  {name:<38} Vb {vb:8.1f}  Vh {vh:6.2f}  share {100 * vh / vb:.3f}%  (Patzke et al. 2015, src {rows and ''}{'own study' if name in ('Diceros bicornus','Loxodonta africana','Hippopotamus amphibius') else 'compilation'})")
for cname, (sci, spec, comps) in REEP.items():
    b = sum(comps) / 1000.0; h = comps[8] / 1000.0
    if b >= 150:
        print(f"  {cname} ({sci}){'':<8} brain {b:8.1f}  hipp {h:6.2f}  share {100 * h / b:.3f}%  (Reep et al. 2007)")
print("\nDiceros bicornus Patzke row check: Mb 531.00 / 1.036 =", round(531.00 / 1.036, 2), "(printed Vb 512.55)")
print(f"Method-offset-adjusted check: line@442.65 = {LINE(442.65):.2f}; x1.58 (Reep>=20cm3 histology offset) = {LINE(442.65) * 1.58:.2f} vs Patzke Vh 7.48 -> {100 * (7.48 - LINE(442.65) * 1.58) / (LINE(442.65) * 1.58):+.1f}%")
