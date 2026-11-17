"""LABEL FORENSICS for the 10 verified catalogue hippocampus labels + the
hippocampus-vs-telencephalon tradeoff. A real hippocampus label should be:
two dominant connected components (L/R), roughly symmetric about the brain
midline, compact. A 'generous' label (sloth bear +160%?) should betray itself
as extra components, one-sided bulk, or spill. Volumes use each file's OWN
zooms (the v2 rule)."""
import nibabel as nib, numpy as np, pandas as pd, os
from scipy import ndimage as ndi
from skimage.filters import threshold_otsu

VERIFIED = ["Ferret", "Red_kangaroo", "Cat", "Cheetah", "Leopard", "Sloth_bear",
            "Giant_panda", "Lion", "Black_rhinoceros", "Giraffe"]

def load(p):
    return nib.load(p)

def brain_midline_x(sp):
    """Midline voxel-x from the species' Atlas mask if present, else Otsu on MRI."""
    base = f"data/brain_catalogue_full/{sp}"
    for cand, is_mask in [(f"{base}/Atlas.nii.gz", True),
                          (f"data/lion/MRI-n4.nii.gz" if sp == "Lion" else f"{base}/MRI-n4.nii.gz", False),
                          (f"{base}/MRI.nii.gz", False)]:
        if not os.path.exists(cand):
            continue
        im = load(cand); d = np.squeeze(np.asanyarray(im.dataobj))
        if is_mask:
            m = d > 0
        else:
            dd = d.astype(np.float32)
            m = ndi.binary_fill_holes(dd > threshold_otsu(dd[dd > 0]))
        xs = np.where(m.any(axis=(1, 2)))[0]
        return (xs.min() + xs.max()) / 2.0, im
    return None, None

rows = []
for sp in VERIFIED:
    p = f"data/brain_catalogue_full/{sp}/Hippocampus.nii.gz"
    if sp == "Lion" and not os.path.exists(p):
        p = "data/lion/atlas/Hippocampus.nii.gz"
    im = load(p)
    d = np.squeeze(np.asanyarray(im.dataobj)) > 0
    vox_cm3 = float(np.prod(im.header.get_zooms()[:3])) / 1000.0
    vol = float(d.sum()) * vox_cm3
    lab, n = ndi.label(d, structure=np.ones((3, 3, 3)))
    sizes = np.sort(ndi.sum(np.ones_like(lab), lab, range(1, n + 1)))[::-1] if n else np.array([])
    top2_frac = float(sizes[:2].sum() / d.sum()) if n else 0.0
    mid, _ = brain_midline_x(sp)
    cents = ndi.center_of_mass(d, lab, range(1, n + 1)) if n else []
    top_idx = np.argsort(ndi.sum(np.ones_like(lab), lab, range(1, n + 1)))[::-1][:2] if n else []
    side = ""
    if mid is not None and len(top_idx) == 2:
        cx = sorted(cents[i][0] for i in top_idx)
        side = f"centroids x={cx[0]:.0f}/{cx[1]:.0f} vs midline {mid:.0f}"
    rows.append(dict(species=sp, vol_cm3=round(vol, 3), n_components=int(n),
                     top1=int(sizes[0]) if n else 0,
                     top2_frac=round(top2_frac, 3), symmetry=side))
    print(f"{sp:<18} vol {vol:6.3f} cm3 | components {n:3d} | top-2 share {top2_frac:5.1%} | {side}")

f = pd.DataFrame(rows)
f.to_csv("outputs/label_forensics.csv", index=False)

print("\n--- hippocampus vs telencephalon (catalogue labels, v3) ---")
v3 = pd.read_csv("outputs/cross_species_volumes_v3.csv")
t = v3[(v3["data_class"] == "catalogue_label") & v3["telencephalon_cm3"].notna()].copy()
t["hipp_of_telen"] = 100 * t["hippocampus_cm3"] / t["telencephalon_cm3"]
t["telen_of_brain"] = 100 * t["telencephalon_cm3"] / t["brain_vol_cm3"]
print(t[["species", "telencephalon_cm3", "hipp_of_telen", "telen_of_brain"]].to_string(index=False))
if len(t) >= 4:
    from scipy import stats
    r = stats.pearsonr(t["telen_of_brain"], t["hipp_of_telen"])
    print(f"pearson r(telencephalon share, hippocampus share of telencephalon) = {r.statistic:.3f} (p {r.pvalue:.3f}, n={len(t)})")
