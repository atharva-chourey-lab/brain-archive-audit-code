"""BLACK RHINOCEROS HIPPOCAMPUS RESIDUAL — investigation (POST-HOC).

The residual was registered in PREDICTION.md section 5 (+80.5%: measured
6.854 cm3 vs 3.80 cm3 predicted by the registered line at the catalogue Atlas
mask volume 442.65 cm3). Everything here is post-hoc relative to that
registration. Tests:
  A. Header / affine integrity of MRI, Atlas mask, Hippocampus label
     (the red-kangaroo lesson: label files can carry copied metadata).
  B. Label forensics round 2: components, L/R split, position, spill checks,
     erosion/dilation boundary sensitivity (felid Test-B style), with the
     lion label run through the identical pipeline as a known-good control.
  C. Denominator: Otsu total-brain volume from the rhino MRI itself
     (volumetry_lion.py method, incl. threshold sensitivity), compared with
     the catalogue Atlas mask the fit used; truncation / coverage checks.
  D. Registered-line predictions and residuals under each denominator.
Writes outputs/segmentations/qc_rhino_hippocampus.png (overlay QC) and
outputs/rhino_boundary_sensitivity.csv.
"""
import nibabel as nib, numpy as np, os, csv
from scipy import ndimage
from scipy.ndimage import binary_dilation, binary_erosion

BASE = "data/brain_catalogue_full/Black_rhinoceros"
MRI_P, ATLAS_P, HIPP_P = f"{BASE}/MRI-n4.nii.gz", f"{BASE}/Atlas.nii.gz", f"{BASE}/Hippocampus.nii.gz"
LINE = lambda brain: 10 ** (-1.6609 + 0.8467 * np.log10(brain))  # registered line, PREDICTION.md s.1

def load(p):
    im = nib.load(p)
    return im, np.squeeze(np.asanyarray(im.dataobj))

print("=" * 78)
print("A. HEADER / AFFINE INTEGRITY")
print("=" * 78)
imgs, arrs = {}, {}
for name, p in (("MRI", MRI_P), ("Atlas", ATLAS_P), ("Hippocampus", HIPP_P)):
    im, d = load(p)
    imgs[name], arrs[name] = im, d
    zooms = tuple(round(float(z), 4) for z in im.header.get_zooms()[:3])
    print(f"{name:<12} shape={im.shape} squeezed={d.shape} zooms={zooms} "
          f"dtype={im.get_data_dtype()} axcodes={nib.aff2axcodes(im.affine)} "
          f"unique_vals={np.unique(d)[:6]}{'...' if len(np.unique(d)) > 6 else ''}")
ref = imgs["MRI"]
for name in ("Atlas", "Hippocampus"):
    same_aff = np.allclose(imgs[name].affine, ref.affine)
    same_shape = imgs[name].shape == ref.shape
    print(f"{name}: affine == MRI affine: {same_aff} | shape == MRI shape: {same_shape}")
vox = float(np.prod(imgs["Hippocampus"].header.get_zooms()[:3])) / 1000.0
vox_mri = float(np.prod(ref.header.get_zooms()[:3])) / 1000.0
print(f"label voxel volume = {vox:.6f} cm3 | MRI voxel volume = {vox_mri:.6f} cm3")

mri = arrs["MRI"].astype(np.float32)
atlas = arrs["Atlas"] > 0
hipp = arrs["Hippocampus"] > 0
assert hipp.shape == atlas.shape == mri.shape, "grid mismatch"
atlas_vol = float(atlas.sum()) * vox_mri
hipp_vol = float(hipp.sum()) * vox
print(f"Atlas mask volume (own zooms): {atlas_vol:.2f} cm3  (v3 table: 442.65)")
print(f"Hippocampus label volume (own zooms): {hipp_vol:.3f} cm3  (registered: 6.854)")
print(f"Hippocampus label volume at MRI zooms: {float(hipp.sum()) * vox_mri:.3f} cm3")
print(f"label voxels outside Atlas mask: {int((hipp & ~atlas).sum())} "
      f"({100.0 * (hipp & ~atlas).sum() / hipp.sum():.2f}% of label)")

print()
print("=" * 78)
print("B. LABEL FORENSICS ROUND 2 — components, symmetry, position")
print("=" * 78)
# midline: axis-0 extent of the Atlas mask (axcodes checked above; axis 0 = L-R)
xs = np.where(atlas.any(axis=(1, 2)))[0]
mid = (xs.min() + xs.max()) / 2.0
print(f"Atlas axis-0 extent {xs.min()}..{xs.max()}, midline x = {mid:.1f}")
for conn_name, structure in (("26-conn", np.ones((3, 3, 3))), ("6-conn", None)):
    lab, n = ndimage.label(hipp, structure=structure)
    sizes = np.array(ndimage.sum(hipp, lab, range(1, n + 1)))
    order = np.argsort(sizes)[::-1]
    cents = ndimage.center_of_mass(hipp, lab, range(1, n + 1))
    top2 = sizes[order[:2]].sum() / hipp.sum()
    print(f"{conn_name}: n_components={n}, total vox={int(hipp.sum())}, top-2 share={top2:.3f}")
    if conn_name == "26-conn":
        for rank, i in enumerate(order[:6]):
            c = cents[i]
            side = "L" if c[0] < mid else "R"
            print(f"  comp#{rank + 1}: {int(sizes[i])} vox = {sizes[i] * vox:.3f} cm3, centroid vox "
                  f"({c[0]:.1f},{c[1]:.1f},{c[2]:.1f}), side {side}, |x-mid|={abs(c[0] - mid):.1f} vox")
        dust = sizes[order[2:]]
        print(f"  dust (components 3..{n}): {len(dust)} comps, {int(dust.sum())} vox total "
              f"= {dust.sum() * vox:.3f} cm3 ({100.0 * dust.sum() / hipp.sum():.2f}% of label), "
              f"largest dust comp {int(dust.max()) if len(dust) else 0} vox")
        # L/R split of the whole label
        left = hipp.copy(); left[int(np.ceil(mid)):, :, :] = False
        right = hipp.copy(); right[:int(np.floor(mid)) + 1, :, :] = False
        print(f"  whole-label split at midline: L {left.sum() * vox:.3f} cm3 / R {right.sum() * vox:.3f} cm3 "
              f"(ratio {left.sum() / right.sum():.3f})")
        # dust adjacency: are dust voxels near the main components or scattered?
        main = np.isin(lab, [order[0] + 1, order[1] + 1])
        dist = ndimage.distance_transform_edt(~main)
        dust_mask = hipp & ~main
        dd = dist[dust_mask]
        print(f"  dust distance to main components: median {np.median(dd):.1f} vox, "
              f"p90 {np.percentile(dd, 90):.1f}, max {dd.max():.1f} vox "
              f"({dd.max() * float(imgs['Hippocampus'].header.get_zooms()[0]):.1f} mm)")
# normalized position of label centroid inside the brain bbox
bb = [np.where(atlas.any(axis=tuple(a for a in range(3) if a != ax)))[0] for ax in range(3)]
cent = ndimage.center_of_mass(hipp)
frac = [(cent[ax] - b.min()) / (b.max() - b.min()) for ax, b in enumerate(bb)]
print(f"label centroid at brain-bbox fractions (ax0 L-R, ax1, ax2): "
      f"{frac[0]:.2f}, {frac[1]:.2f}, {frac[2]:.2f}")
hb = [np.where(hipp.any(axis=tuple(a for a in range(3) if a != ax)))[0] for ax in range(3)]
print(f"label bbox (vox): " + "; ".join(f"ax{ax} {b.min()}..{b.max()} (of brain {bb[ax].min()}..{bb[ax].max()})" for ax, b in enumerate(hb)))

print()
print("=" * 78)
print("B2. BOUNDARY SENSITIVITY (felid Test-B style) — rhino + lion control")
print("=" * 78)
def boundary(label_arr, constraint, vox_cm3, tag):
    v0 = float(label_arr.sum()) * vox_cm3
    ero = binary_erosion(label_arr) & constraint
    out = {"species": tag, "catalogue_cm3": round(v0, 3)}
    out["erode1_cm3"] = round(float(ero.sum()) * vox_cm3, 3)
    out["erode1_pct"] = round(100.0 * (float(ero.sum()) * vox_cm3 - v0) / v0, 1)
    for k in (1, 2):
        dil = binary_dilation(label_arr, iterations=k) & constraint
        out[f"plus{k}vox_cm3"] = round(float(dil.sum()) * vox_cm3, 3)
        out[f"plus{k}vox_pct"] = round(100.0 * (float(dil.sum()) * vox_cm3 - v0) / v0, 1)
    print(f"{tag}: base {v0:.3f} | erode1 {out['erode1_cm3']} ({out['erode1_pct']:+.1f}%) | "
          f"+1vox {out['plus1vox_cm3']} ({out['plus1vox_pct']:+.1f}%) | +2vox {out['plus2vox_cm3']} ({out['plus2vox_pct']:+.1f}%)")
    return out
rows = [boundary(hipp, atlas, vox, "Black_rhinoceros")]
lim, lion_lab = load("data/lion/atlas/Hippocampus.nii.gz")
_, lion_tel = load("data/lion/atlas/Telencephalon.nii.gz")
lvox = float(np.prod(lim.header.get_zooms()[:3])) / 1000.0
rows.append(boundary(lion_lab > 0, lion_tel > 0, lvox, "Lion (control)"))
with open("outputs/rhino_boundary_sensitivity.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("wrote outputs/rhino_boundary_sensitivity.csv")

print()
print("=" * 78)
print("C. DENOMINATOR — Otsu total brain from the rhino MRI (lion method)")
print("=" * 78)
nz = mri[mri > 0]
hist, edges = np.histogram(nz, bins=256)
w = hist / hist.sum(); omega = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
mu_t = mu[-1]
sigma_b2 = (mu_t * omega - mu) ** 2 / (omega * (1 - omega) + 1e-12)
thr0 = float(edges[int(np.nanargmax(sigma_b2))])
print(f"Otsu threshold = {thr0:.1f} (MRI range {mri.min():.0f}..{mri.max():.0f})")
def vol_at(thr):
    m = ndimage.binary_fill_holes(mri > thr)
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)
otsu_masks = {}
for f in (0.8, 0.9, 1.0, 1.1, 1.2):
    m = vol_at(thr0 * f)
    otsu_masks[f] = m
    print(f"  x{f}: {float(m.sum()) * vox_mri:.1f} cm3")
otsu = otsu_masks[1.0]
inter = float((atlas & otsu).sum()); union = float((atlas | otsu).sum())
print(f"Atlas {atlas_vol:.1f} vs Otsu@1.0 {float(otsu.sum()) * vox_mri:.1f}: Dice {2 * inter / (atlas.sum() + otsu.sum()):.3f}; "
      f"atlas-only {float((atlas & ~otsu).sum()) * vox_mri:.1f} cm3; otsu-only {float((otsu & ~atlas).sum()) * vox_mri:.1f} cm3")
for ax in range(3):
    a = np.where(atlas.any(axis=tuple(x for x in range(3) if x != ax)))[0]
    o = np.where(otsu.any(axis=tuple(x for x in range(3) if x != ax)))[0]
    nzm = np.where((mri > 0).any(axis=tuple(x for x in range(3) if x != ax)))[0]
    print(f"  axis {ax}: atlas {a.min()}..{a.max()} | otsu {o.min()}..{o.max()} | MRI nonzero {nzm.min()}..{nzm.max()} | grid {mri.shape[ax]}")
print(f"  masks touch grid border? atlas: {any([atlas[0].any(), atlas[-1].any(), atlas[:, 0].any(), atlas[:, -1].any(), atlas[:, :, 0].any(), atlas[:, :, -1].any()])}, "
      f"otsu: {any([otsu[0].any(), otsu[-1].any(), otsu[:, 0].any(), otsu[:, -1].any(), otsu[:, :, 0].any(), otsu[:, :, -1].any()])}")

print()
print("=" * 78)
print("D. PREDICTIONS / RESIDUALS UNDER EACH DENOMINATOR (registered line)")
print("=" * 78)
for tag, brain in (("catalogue Atlas mask (as fitted)", atlas_vol),
                   ("Otsu @1.0 (this script)", float(otsu.sum()) * vox_mri),
                   ("Otsu @0.9", float(otsu_masks[0.9].sum()) * vox_mri),
                   ("Otsu @1.1", float(otsu_masks[1.1].sum()) * vox_mri),
                   ("Patzke 2015 specimen Vb (different animal)", 512.55)):
    pred = LINE(brain)
    print(f"  {tag:<44} brain {brain:7.1f} -> predicted {pred:.2f}, measured 6.854, "
          f"residual {100.0 * (hipp_vol - pred) / pred:+.1f}%, hipp share {100.0 * hipp_vol / brain:.3f}%")

# ---------------------------------------------------------------- overlay QC
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
cx, cy, cz = [int(round(c)) for c in cent]
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for axp, (sl, ttl) in zip(axes, [(mri[:, :, cz], "axial (ax2)"), (mri[:, cy, :], "coronal (ax1)"), (mri[cx, :, :], "sagittal (ax0)")]):
    axp.imshow(np.rot90(sl), cmap="gray")
    lab_sl = [hipp[:, :, cz], hipp[:, cy, :], hipp[cx, :, :]][list(axes).index(axp)]
    msk = np.ma.masked_where(np.rot90(lab_sl) == 0, np.rot90(lab_sl))
    axp.imshow(msk, cmap="Reds", alpha=0.85)
    axp.set_title(f"rhino hippocampus label — {ttl} through centroid"); axp.axis("off")
os.makedirs("outputs/segmentations", exist_ok=True)
fig.tight_layout(); fig.savefig("outputs/segmentations/qc_rhino_hippocampus.png", dpi=90)
print("\nwrote outputs/segmentations/qc_rhino_hippocampus.png")
