"""Lion total brain volume with threshold-sensitivity analysis.
Brain Catalogue / Zenodo 44855, ex vivo structural MRI, 0.3 mm iso, uint8.
Method: Otsu threshold on non-zero voxels; sensitivity at 0.8x/0.9x/1.1x/1.2x Otsu;
largest connected component + hole filling at each level."""
import nibabel as nib, numpy as np, pandas as pd
from scipy import ndimage

img = nib.load("data/lion/MRI-n4.nii.gz")
d = img.get_fdata(dtype=np.float32)
vv = float(np.prod(img.header.get_zooms())) / 1000.0  # cm^3
nz = d[d > 0]
hist, edges = np.histogram(nz, bins=256)
w = hist / hist.sum(); omega = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
mu_t = mu[-1]
sigma_b2 = (mu_t * omega - mu) ** 2 / (omega * (1 - omega) + 1e-12)
thr0 = float(edges[int(np.nanargmax(sigma_b2))])

def vol_at(thr):
    m = ndimage.binary_fill_holes(d > thr)
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    m = lab == (int(np.argmax(sizes)) + 1)
    return float(m.sum() * vv), m

rows = []
for f in (0.8, 0.9, 1.0, 1.1, 1.2):
    v, m = vol_at(thr0 * f)
    rows.append({"threshold_factor": f, "threshold_value": round(thr0 * f, 1), "volume_cm3": round(v, 1)})
    if f == 1.0:
        np.save("outputs/lion_brainmask_otsu.npy", m)
df = pd.DataFrame(rows)
df.to_csv("outputs/lion_volume_sensitivity.csv", index=False)
print(f"Otsu threshold = {thr0:.1f}")
print(df.to_string(index=False))
