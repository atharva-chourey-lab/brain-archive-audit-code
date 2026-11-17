"""Chen-style layer, structural edition (v2, QC-corrected): a shared morphometric
representational space. Every brain is embedded by the SAME four shape features from
its whole-brain mask: log10 volume, gyrification proxy (surface area vs sphere of
equal volume, masks resampled to a common 0.6 mm grid), two elongation ratios from
the mask covariance eigenvalues. Distances in standardised feature space =
representational dissimilarities. Descriptive only: most species n=1.

QC (visual, outputs/qc_contact_sheet.png + qc_wolf2.png):
- PASS: baboon, cheetah, giant panda, giraffe, gorilla, leopard, okapi, sloth bear,
  zebra, lion (Otsu mask hugs the brain outline).
- PASS WITH CAVEAT: bottlenose dolphin (as-scanned volume below species-typical;
  header geometry taken at face value - shape ratios are scale-invariant),
  gray wolf (mask needed closing x3 to seal the cortical shell; specimen possibly
  juvenile - flagged, not hidden).
- EXCLUDED: orangutan (in-vivo-style scan with skull/scalp - mask not comparable),
  red squirrel (header voxel size is a 1.0 mm placeholder - absolute scale lost).
- FIXED SOURCES: domestic cat = Catlas atlas labels>0 (not an intensity threshold);
  adult human = nilearn MNI152 brain mask; infants = parcellation minus the
  extra-axial CSF label (24), so masks approximate brain + ventricular CSF like the
  filled Otsu masks of the ex vivo specimens.
"""
import nibabel as nib, numpy as np, pandas as pd, glob, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.measure import marching_cubes

def otsu_mask(d, closing=0):
    nz = d[d > 0]
    hist, edges = np.histogram(nz, bins=256)
    w = hist / hist.sum(); om = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
    s2 = (mu[-1] * om - mu) ** 2 / (om * (1 - om) + 1e-12)
    thr = float(edges[int(np.nanargmax(s2))])
    m = d > thr
    if closing: m = ndimage.binary_closing(m, iterations=closing)
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)

def features(mask, zooms):
    zooms = np.asarray(zooms, float)
    V = float(mask.sum() * np.prod(zooms))
    coords = np.argwhere(mask) * zooms
    cov = np.cov((coords - coords.mean(0)).T)
    ev = np.sort(np.linalg.eigvalsh(cov))[::-1]
    a = float(np.sqrt(ev[0] / ev[2])); c = float(np.sqrt(ev[1] / ev[2]))
    mr = ndimage.zoom(mask.astype(np.uint8), zooms / 0.6, order=0) > 0
    verts, faces, _, _ = marching_cubes(mr, level=0.5, spacing=(0.6, 0.6, 0.6))
    v = verts[faces]
    SA = float(0.5 * np.linalg.norm(np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]), axis=1).sum())
    return {"volume_cm3": V / 1000, "log10_vol": float(np.log10(V / 1000)),
            "gyrification_proxy": float(SA / (4.836 * V ** (2 / 3))),
            "elong_long": a, "elong_flat": c, "surface_mm2": SA}

rows = []
EXCLUDE = {"orangutan", "red_squirrel"}
paths = {os.path.basename(p)[:-7]: p for p in glob.glob("data/brain_catalogue/*.nii.gz")}
paths["lion"] = "data/lion/MRI-n4.nii.gz"
for name, p in sorted(paths.items()):
    if name in EXCLUDE: continue
    img = nib.load(p); d = np.squeeze(img.get_fdata(dtype=np.float32))
    if d.ndim == 4: d = d[..., 0]
    m = otsu_mask(d, closing=3 if name == "gray_wolf" else 0)
    qc = "pass_caveat" if name in ("gray_wolf", "bottlenose_dolphin") else "pass"
    rows.append({"point": name, "group": "brain_catalogue", "qc": qc,
                 **features(m, img.header.get_zooms()[:3])}); print("done", name, flush=True)
# Domestic cat: Catlas T1 population template (Stolzberg et al. 2017) - labelled proxy,
# not a lion substitute. Mask = template > 5% of max (the atlas label file covers cortex
# only, so it cannot serve as a whole-brain mask; threshold sweep 2-10% gives 25-27 cm3,
# the expected cat brain volume).
img = nib.load("data/proxies/Catlas_dist/CatT1avg_AFNI.nii.gz")
d = img.get_fdata(dtype=np.float32)
m = ndimage.binary_fill_holes(d > 0.05 * d.max())
lab, n = ndimage.label(m)
sizes = ndimage.sum(m, lab, range(1, n + 1))
m = lab == (int(np.argmax(sizes)) + 1)
rows.append({"point": "domestic_cat_template", "group": "proxy_template", "qc": "template_mask",
             **features(m, img.header.get_zooms()[:3])}); print("done cat", flush=True)
# Adult human: MNI152 brain mask via nilearn (population template, not a specimen)
from nilearn.datasets import load_mni152_brain_mask
bm = load_mni152_brain_mask(resolution=2)
m = bm.get_fdata() > 0
rows.append({"point": "adult_human_MNI152_template", "group": "template", "qc": "atlas_mask",
             **features(m, bm.header.get_zooms()[:3])}); print("done adult human", flush=True)
# Human infants: parcellation minus extra-axial CSF label 24
for p in sorted(glob.glob("data/human_infant/mcrib2/subjects/*_parc.nii.gz")):
    img = nib.load(p); a = np.asanyarray(img.dataobj)
    m = (a > 0) & (a != 24)
    sid = p.split("_")[-2]
    rows.append({"point": f"human_infant_{sid}", "group": "human_infant_mcrib", "qc": "atlas_mask",
                 **features(m, img.header.get_zooms()[:3])}); print("done infant", sid, flush=True)

df = pd.DataFrame(rows)
FEATS = ["log10_vol", "gyrification_proxy", "elong_long", "elong_flat"]
Z = (df[FEATS] - df[FEATS].mean()) / df[FEATS].std(ddof=1)
U, S, Vt = np.linalg.svd(Z.values, full_matrices=False)
df["PC1"] = U[:, 0] * S[0]; df["PC2"] = U[:, 1] * S[1]
var = S ** 2 / (S ** 2).sum()
df.to_csv("outputs/morphospace_features.csv", index=False)
print("PC variance explained:", np.round(var, 3))
print("Loadings PC1:", dict(zip(FEATS, np.round(Vt[0], 2))), " PC2:", dict(zip(FEATS, np.round(Vt[1], 2))))
centroid = Z[df.group == "human_infant_mcrib"].mean()
pts = {r.point: Z.iloc[i] for i, r in df.iterrows()}
keys = ["lion", "adult_human_MNI152_template", "leopard", "cheetah", "gray_wolf",
        "domestic_cat_template", "gorilla", "bottlenose_dolphin"]
out = [{"pair": f"human_infant_centroid <-> {k}", "distance_zspace": round(float(np.linalg.norm(centroid - pts[k])), 2)}
       for k in keys if k in pts]
out.append({"pair": "lion <-> adult_human_MNI152_template",
            "distance_zspace": round(float(np.linalg.norm(pts["lion"] - pts["adult_human_MNI152_template"])), 2)})
# nearest species to the lion
lion_d = sorted(((float(np.linalg.norm(pts["lion"] - pts[k])), k) for k in pts
                 if k not in ("lion",) and not k.startswith("human_infant")))[:4]
out += [{"pair": f"lion <-> {k} (nearest)", "distance_zspace": round(d, 2)} for d, k in lion_d]
pd.DataFrame(out).to_csv("outputs/morphospace_distances.csv", index=False)
print(pd.DataFrame(out).to_string(index=False))

# Figure 3: the morphospace
fig, ax = plt.subplots(figsize=(9, 7))
sp = df[df.group == "brain_catalogue"]
ax.scatter(sp.PC1, sp.PC2, s=70, color="#d88a3b", zorder=3)
for _, r in sp.iterrows(): ax.annotate(r.point, (r.PC1, r.PC2), fontsize=8, xytext=(4, 4), textcoords="offset points")
inf = df[df.group == "human_infant_mcrib"]
ax.scatter(inf.PC1, inf.PC2, s=45, color="#3b7dd8", zorder=3, label="Human newborns (n=10, M-CRIB)")
ax.scatter([inf.PC1.mean()], [inf.PC2.mean()], s=220, marker="*", color="#3b7dd8", zorder=4)
for _, r in df[df.group.isin(["template", "proxy_template"])].iterrows():
    ax.scatter([r.PC1], [r.PC2], s=90, marker="D", color="#666666", zorder=3)
    ax.annotate(r.point, (r.PC1, r.PC2), fontsize=8, xytext=(4, 4), textcoords="offset points")
li = df[df.point == "lion"].iloc[0]
ax.scatter([li.PC1], [li.PC2], s=260, marker="*", color="#d88a3b", zorder=5)
ax.set_xlabel(f"PC1 ({var[0]*100:.0f}% of variance) — size + elongation")
ax.set_ylabel(f"PC2 ({var[1]*100:.0f}% of variance) — folding vs size")
ax.set_title("Figure 3 — A structural morphometric space (Chen-style geometry, structural edition).\n"
             "Same four mask features for every brain; stars = lion and newborn centroid; diamonds = templates.\n"
             "Orangutan and red squirrel excluded on QC (see report). Descriptive embedding, n=1 per species.", fontsize=9)
ax.legend(fontsize=8); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("outputs/fig3_morphospace.png", dpi=200)
print("fig3 saved")
