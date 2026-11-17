"""Rhino label shape deep-dive (post-hoc follow-up to rhino_investigation.py):
per-component geometry, coronal-plane content at the centroid slice, column
thickness along S-I, and RGB-overlay montages. The centroid coronal overlay
suggested slab-like geometry that the component summary could not see."""
import nibabel as nib, numpy as np, os
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "data/brain_catalogue_full/Black_rhinoceros"
mri = np.squeeze(np.asanyarray(nib.load(f"{BASE}/MRI-n4.nii.gz").dataobj)).astype(np.float32)
hipp = np.squeeze(np.asanyarray(nib.load(f"{BASE}/Hippocampus.nii.gz").dataobj)) > 0
atlas = np.squeeze(np.asanyarray(nib.load(f"{BASE}/Atlas.nii.gz").dataobj)) > 0
vox = 0.45 ** 3 / 1000.0

lab, n = ndimage.label(hipp, structure=np.ones((3, 3, 3)))
sizes = np.array(ndimage.sum(hipp, lab, range(1, n + 1)))
order = np.argsort(sizes)[::-1]
print(f"total label vox {hipp.sum()}, components {n}")
for rank, i in enumerate(order[:2]):
    m = lab == (i + 1)
    bb = [np.where(m.any(axis=tuple(a for a in range(3) if a != ax)))[0] for ax in range(3)]
    c = ndimage.center_of_mass(m)
    print(f"comp#{rank + 1}: {int(sizes[i])} vox = {sizes[i] * vox:.3f} cm3, centroid "
          f"({c[0]:.1f},{c[1]:.1f},{c[2]:.1f}), bbox " +
          "; ".join(f"ax{ax} {b.min()}..{b.max()} ({(b.max() - b.min() + 1) * 0.45:.1f} mm)" for ax, b in enumerate(bb)))

# coronal plane through whole-label centroid (ax1 = 166)
cy = 166
plane = hipp[:, cy, :]
print(f"\ncoronal plane ax1={cy}: label vox {plane.sum()}, "
      f"ax0 extent {np.where(plane.any(axis=1))[0].min()}..{np.where(plane.any(axis=1))[0].max()}, "
      f"ax2 extent {np.where(plane.any(axis=0))[0].min()}..{np.where(plane.any(axis=0))[0].max()}")
cols = [np.where(plane[x, :])[0] for x in range(plane.shape[0])]
spans = [len(c) for c in cols if len(c)]
print(f"label columns in plane: {len(spans)}, ax2 span per column: median {np.median(spans):.0f} vox "
      f"({np.median(spans) * 0.45:.1f} mm), max {max(spans)} vox ({max(spans) * 0.45:.1f} mm)")

# A-P profile: label voxels per coronal slice
prof = hipp.sum(axis=(0, 2))
nz = np.where(prof > 0)[0]
print(f"\nA-P profile: label present ax1 {nz.min()}..{nz.max()} ({(nz.max() - nz.min() + 1) * 0.45:.0f} mm); "
      f"peak slice ax1={int(np.argmax(prof))} with {int(prof.max())} vox")
for a in range(0, 328, 20):
    print(f"  ax1 {a:3d}: {int(prof[a]):5d} vox {'#' * int(60 * prof[a] / prof.max())}")
# S-I profile
profz = hipp.sum(axis=(0, 1))
nzz = np.where(profz > 0)[0]
print(f"S-I profile: label present ax2 {nzz.min()}..{nzz.max()}; peak ax2={int(np.argmax(profz))} ({int(profz.max())} vox)")

# column thickness along ax2 across the whole label
thickness = []
for x in range(hipp.shape[0]):
    for y in range(hipp.shape[1]):
        col = np.where(hipp[x, y, :])[0]
        if len(col):
            thickness.append(col.max() - col.min() + 1)
thickness = np.array(thickness)
print(f"\nax2 column span over all label columns: median {np.median(thickness):.0f} vox "
      f"({np.median(thickness) * 0.45:.1f} mm), p90 {np.percentile(thickness, 90):.0f} vox "
      f"({np.percentile(thickness, 90) * 0.45:.1f} mm), max {thickness.max()} vox ({thickness.max() * 0.45:.1f} mm)")

def rgb_overlay(base, mask, color=(255, 40, 40)):
    b = np.clip(base / np.percentile(base[base > 0], 99) * 255, 0, 255).astype(np.uint8)
    rgb = np.stack([b] * 3, axis=-1)
    rgb[mask] = color
    return rgb

os.makedirs("outputs/segmentations", exist_ok=True)
fig, axes = plt.subplots(2, 5, figsize=(20, 8))
for j, a in enumerate([110, 140, 166, 195, 225]):
    axes[0, j].imshow(np.rot90(rgb_overlay(mri[:, a, :], hipp[:, a, :])))
    axes[0, j].set_title(f"coronal ax1={a}"); axes[0, j].axis("off")
for j, z in enumerate([60, 80, 95, 110, 125]):
    axes[1, j].imshow(np.rot90(rgb_overlay(mri[:, :, z], hipp[:, :, z])))
    axes[1, j].set_title(f"axial ax2={z}"); axes[1, j].axis("off")
fig.tight_layout(); fig.savefig("outputs/segmentations/qc_rhino_montage.png", dpi=80)
print("wrote outputs/segmentations/qc_rhino_montage.png")

# sagittal montage through each main component centroid
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for j, i in enumerate(order[:2]):
    m = lab == (i + 1)
    cx = int(round(ndimage.center_of_mass(m)[0]))
    axes[j].imshow(np.rot90(rgb_overlay(mri[cx, :, :], hipp[cx, :, :])))
    axes[j].set_title(f"sagittal ax0={cx} (comp#{j + 1} centroid)"); axes[j].axis("off")
fig.tight_layout(); fig.savefig("outputs/segmentations/qc_rhino_sagittal.png", dpi=90)
print("wrote outputs/segmentations/qc_rhino_sagittal.png")
