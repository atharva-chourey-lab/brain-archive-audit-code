import nibabel as nib, numpy as np, glob
from scipy import ndimage
def vol(mask, zooms): return float(mask.sum()*np.prod(zooms))/1000
def largest(m):
    m = ndimage.binary_fill_holes(m); lab, n = ndimage.label(m)
    if n == 0: return m
    return lab == (int(np.argmax(ndimage.sum(m, lab, range(1, n+1)))) + 1)
for p in sorted(glob.glob("data/brain_catalogue/*.nii.gz")) + ["data/lion/MRI-n4.nii.gz"]:
    img = nib.load(p); d = np.squeeze(img.get_fdata(dtype=np.float32))
    if d.ndim == 4: d = d[..., 0]
    z = img.header.get_zooms()[:3]; nz = d[d > 0]
    row = {"file": p.split("/")[-1], "shape": str(d.shape), "zoom": [round(float(x),3) for x in z],
           "nonzero_frac": round(float((d > 0).mean()), 3)}
    for name, thr in [("p05", np.percentile(nz, 5)), ("p25", np.percentile(nz, 25)), ("p50", np.percentile(nz, 50))]:
        row[f"vol_gt_{name}"] = round(vol(largest(d > thr), z), 1)
    print(row)
