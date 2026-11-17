import nibabel as nib, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

img = nib.load("data/brain_catalogue/gray_wolf.nii.gz")
d = np.squeeze(img.get_fdata(dtype=np.float32)); z = img.header.get_zooms()[:3]
nz = d[d > 0]
hist, edges = np.histogram(nz, bins=256)
w = hist / hist.sum(); om = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
s2 = (mu[-1] * om - mu) ** 2 / (om * (1 - om) + 1e-12)
otsu = float(edges[int(np.nanargmax(s2))])

def mask_ci(ci):
    m = d > otsu
    if ci: m = ndimage.binary_closing(m, iterations=ci)
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)

fig, axes = plt.subplots(1, 4, figsize=(16, 5))
for ax, ci in zip(axes, [0, 1, 2, 3]):
    m = mask_ci(ci)
    v = m.sum() * np.prod(z) / 1000
    zz = m.shape[2] // 2
    ax.imshow(np.rot90(d[:, :, zz]), cmap="gray")
    ax.contour(np.rot90(m[:, :, zz]), levels=[0.5], colors="red", linewidths=0.7)
    ax.set_title(f"closing {ci}: {v:.0f} cm3"); ax.axis("off")
fig.savefig("outputs/qc_wolf2.png", dpi=120); print("saved")
