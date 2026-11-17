import nibabel as nib, numpy as np, json
p = "data/lion/MRI-n4.nii.gz"
img = nib.load(p)
d = img.get_fdata(dtype=np.float32)
zooms = img.header.get_zooms()
vox_vol = float(np.prod(zooms))
nz = d[d > 0]
print(json.dumps({
  "shape": list(img.shape), "zooms_mm": [float(z) for z in zooms],
  "dtype": str(img.get_data_dtype()), "vox_vol_mm3": vox_vol,
  "intensity_min": float(d.min()), "intensity_max": float(d.max()),
  "nonzero_voxels": int((d > 0).sum()),
  "p1": float(np.percentile(nz, 1)), "p50": float(np.percentile(nz, 50)),
  "p99": float(np.percentile(nz, 99)),
}, indent=1))
# crude first-pass brain mask: Otsu-like threshold on nonzero voxels
from scipy import ndimage
hist, edges = np.histogram(nz, bins=256)
# Otsu
w = hist / hist.sum(); omega = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
mu_t = mu[-1]; sigma_b2 = (mu_t * omega - mu) ** 2 / (omega * (1 - omega) + 1e-12)
t_idx = int(np.nanargmax(sigma_b2)); thr = float(edges[t_idx])
mask = d > thr
mask = ndimage.binary_fill_holes(mask)
lab, n = ndimage.label(mask)
if n > 1:
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    mask = lab == (int(np.argmax(sizes)) + 1)
vol_mm3 = float(mask.sum() * vox_vol)
print(f"OTSU thr={thr:.2f}  brain-mask voxels={int(mask.sum())}  volume={vol_mm3:,.0f} mm^3 = {vol_mm3/1000:.1f} cm^3")
np.save("outputs/lion_brainmask_v0.npy", mask)
