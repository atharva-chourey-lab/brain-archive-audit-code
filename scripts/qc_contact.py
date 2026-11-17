import nibabel as nib, numpy as np, glob, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

def otsu_mask(d):
    nz = d[d > 0]
    hist, edges = np.histogram(nz, bins=256)
    w = hist / hist.sum(); om = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
    s2 = (mu[-1] * om - mu) ** 2 / (om * (1 - om) + 1e-12)
    thr = float(edges[int(np.nanargmax(s2))])
    m = ndimage.binary_fill_holes(d > thr)
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)

paths = sorted(glob.glob("data/brain_catalogue/*.nii.gz")) + ["data/lion/MRI-n4.nii.gz"]
fig, axes = plt.subplots(3, 5, figsize=(16, 10))
for ax, p in zip(axes.flat, paths):
    img = nib.load(p); d = np.squeeze(img.get_fdata(dtype=np.float32))
    if d.ndim == 4: d = d[..., 0]
    m = otsu_mask(d)
    z = m.shape[2] // 2
    ax.imshow(np.rot90(d[:, :, z]), cmap="gray")
    ax.contour(np.rot90(m[:, :, z]), levels=[0.5], colors="red", linewidths=0.7)
    v = m.sum() * np.prod(img.header.get_zooms()[:3]) / 1000
    ax.set_title(f"{os.path.basename(p)[:-7]}  {v:.0f} cm3", fontsize=9); ax.axis("off")
for ax in axes.flat[len(paths):]: ax.axis("off")
fig.suptitle("QC contact sheet — mid-axial slice, red = current Otsu mask")
fig.tight_layout(); fig.savefig("outputs/qc_contact_sheet.png", dpi=130)
print("saved")
