"""Cross-species volumes from the Brain Catalogue's own segmentation files.
For every species in data/brain_catalogue_full/: brain volume from an Otsu mask of
its MRI (same method as the lion v0), and volumes of every atlas label file the
catalogue hosts (Hippocampus, Telencephalon/Cerebrum, Striatum, Cerebellum,
Corpus_callosum, Neocortex, Atlas). Hippocampus SHARE uses voxel-count ratio, so it
stays valid even where a header's absolute scale is wrong. QC contact sheet saved."""
import nibabel as nib, numpy as np, pandas as pd, os, json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

ROOT = "data/brain_catalogue_full"
inv = json.load(open("outputs/braincatalogue_inventory.json"))

def otsu_mask(d):
    nz = d[d > 0]
    if len(nz) == 0: return None
    hist, edges = np.histogram(nz, bins=256)
    w = hist / hist.sum(); om = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
    s2 = (mu[-1] * om - mu) ** 2 / (om * (1 - om) + 1e-12)
    thr = float(edges[int(np.nanargmax(s2))])
    m = ndimage.binary_fill_holes(d > thr)
    lab, n = ndimage.label(m)
    if n == 0: return m
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)

rows = []
fig, axes = plt.subplots(7, 6, figsize=(20, 24))
axes = axes.flat
for i, (species, v) in enumerate(sorted(inv.items())):
    sdir = os.path.join(ROOT, species)
    brain_file = v.get("brain")
    row = {"species": species}
    try:
        img = nib.load(os.path.join(sdir, brain_file))
        d = np.squeeze(img.get_fdata(dtype=np.float32))
        if d.ndim == 4: d = d[..., 0]
        zooms = np.array(img.header.get_zooms()[:3], float)
        vox_cm3 = float(np.prod(zooms)) / 1000.0
        mask = otsu_mask(d)
        brain_vox = int(mask.sum())
        row["brain_vol_cm3_otsu"] = round(brain_vox * vox_cm3, 2)
        row["zooms"] = "x".join(str(z) for z in zooms)
        for lf in v.get("atlas", []):
            p = os.path.join(sdir, lf)
            if not os.path.exists(p): row[lf[:-7].lower() + "_cm3"] = None; continue
            a = np.asanyarray(nib.load(p).dataobj)
            labs = np.unique(a)
            nvox = int((a > 0).sum())
            key = lf[:-7].lower()
            row[key + "_cm3"] = round(nvox * vox_cm3, 3)
            if key == "hippocampus":
                row["hippocampus_pct_of_brain"] = round(100 * nvox / brain_vox, 2) if brain_vox else None
            if key == "atlas":
                row["atlas_label_values"] = ",".join(str(int(x)) for x in labs[:20])
                row["atlas_n_labels"] = len(labs) - 1
        rows.append(row)
        # QC panel: mid-slice with hippocampus overlay if present
        ax = axes[i]
        hp = os.path.join(sdir, "Hippocampus.nii.gz")
        zz = d.shape[2] // 2
        ax.imshow(np.rot90(d[:, :, zz]), cmap="gray")
        ax.contour(np.rot90(mask[:, :, zz]), levels=[0.5], colors="cyan", linewidths=0.5)
        if os.path.exists(hp):
            a = np.asanyarray(nib.load(hp).dataobj)
            zbest = int(np.argmax([(a[:, :, k] > 0).sum() for k in range(a.shape[2])]))
            ax.imshow(np.rot90(d[:, :, zbest]), cmap="gray")
            ax.contour(np.rot90(mask[:, :, zbest]), levels=[0.5], colors="cyan", linewidths=0.5)
            ax.imshow(np.ma.masked_where(np.rot90(a[:, :, zbest]) == 0, np.rot90(a[:, :, zbest])),
                      cmap="Reds", alpha=0.8, interpolation="nearest")
        ax.set_title(species, fontsize=9); ax.axis("off")
    except Exception as e:
        row["error"] = str(e)[:120]; rows.append(row)
        axes[i].set_title(species + " ERROR", fontsize=9); axes[i].axis("off")
for j in range(len(rows), 42): axes[j].axis("off")
fig.suptitle("QC sheet 2 — brain mask (cyan) + hippocampus label (red) per species", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.99]); fig.savefig("outputs/qc_contact_sheet2.png", dpi=110)
df = pd.DataFrame(rows)
df.to_csv("outputs/cross_species_volumes.csv", index=False)
cols = [c for c in ["species", "brain_vol_cm3_otsu", "hippocampus_cm3", "hippocampus_pct_of_brain",
                    "telencephalon_cm3", "cerebrum_cm3", "striatum_cm3", "cerebellum_cm3",
                    "corpus_callosum_cm3", "neocortex_cm3", "atlas_n_labels"] if c in df]
print(df[cols].to_string(index=False))
print("\nspecies processed:", len(df))
