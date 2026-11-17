"""IDENTIFY the hippocampus in the SBA CIVM rhesus v1 labels — v2, component-based.
v1 wrongly assumed L/R split labels; the file's posterior-ventral candidates all
sit at RAS x ~ 0, i.e. bilateral structures carried as SINGLE labels. The test
therefore works in voxel space: a hippocampus label = exactly 2 dominant
connected components of similar size, mirrored about the brain's axis-0 centre,
in the posterior-ventral quadrant. Candidates are overlaid on the b0 in three
planes; the picture, not the table, accepts or rejects."""
import os
import nibabel as nib, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

GOLD = os.environ.get("SBA_MACAQUE_DIR", "sba-macaque")  # local path to the CIVM/SBA macaque atlas download (not redistributed)
lab_im = nib.load(f"{GOLD}/civm_rhesus_v1_labels.nii.gz")
b0_im = nib.load(f"{GOLD}/civm_rhesus_v1_b0.nii.gz")
lab = np.asanyarray(lab_im.dataobj)
vox_cm3 = float(np.prod(lab_im.header.get_zooms()[:3])) / 1000.0
mask = lab > 0
centre = np.array(ndi.center_of_mass(mask))
print(f"brain centre (voxel) {np.round(centre,1)}; labelled volume {mask.sum()*vox_cm3:.1f} cm3")

vals, counts = np.unique(lab[mask], return_counts=True)
print("\nlabels with total volume 0.30-1.60 cm3 and exactly 2 dominant components:")
found = []
for v, c in zip(vals, counts):
    vol = c * vox_cm3
    if not (0.30 <= vol <= 1.60):
        continue
    sel = lab == v
    cc, n = ndi.label(sel, structure=np.ones((3, 3, 3)))
    if n < 2:
        continue
    sizes = ndi.sum(np.ones_like(cc), cc, range(1, n + 1))
    order = np.argsort(sizes)[::-1]
    top2 = sizes[order[:2]]
    if top2.sum() / c < 0.9 or top2.min() / top2.max() < 0.5:
        continue
    cents = ndi.center_of_mass(sel, cc, range(1, n + 1))
    c1, c2 = np.array(cents[order[0]]), np.array(cents[order[1]])
    mirror_err = abs((c1[0] + c2[0]) / 2 - centre[0])
    print(f"  label {int(v):3d}: total {vol:.3f} cm3 | comps {int(top2[0])}/{int(top2[1])} vox | "
          f"centroids {np.round(c1,0)} / {np.round(c2,0)} | axis0 mirror err {mirror_err:.1f} vox")
    found.append((int(v), vol, c1, c2))

b0 = np.asanyarray(b0_im.dataobj).astype(np.float32)
for v, vol, c1, c2 in found:
    sel = lab == v
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    zz = int(round((c1[2] + c2[2]) / 2)); yy = int(round((c1[1] + c2[1]) / 2)); xx = int(round((c1[0] + c2[0]) / 2))
    for ax, sl, ttl in [(axes[0], np.s_[ :, :, zz], f"axial z={zz}"), (axes[1], np.s_[:, yy, :], f"coronal y={yy}"), (axes[2], np.s_[xx, :, :], f"sagittal x={xx}")]:
        ax.imshow(np.rot90(b0[sl]), cmap="gray")
        ax.imshow(np.ma.masked_where(np.rot90(sel[sl]) == 0, np.rot90(sel[sl])), cmap="Reds", alpha=0.8, interpolation="nearest")
        ax.set_title(f"label {v} — {ttl}"); ax.axis("off")
    fig.savefig(f"outputs/segmentations/qc_civm_label_{v}.png", dpi=110)
    print(f"  overlay saved: outputs/segmentations/qc_civm_label_{v}.png")
