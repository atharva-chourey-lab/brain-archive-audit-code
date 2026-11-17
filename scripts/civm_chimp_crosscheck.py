"""CIVM -> CHIMPANZEE hippocampus cross-check (model-estimated, cross-check ONLY).

Purpose: the D99 macaque-atlas propagation gave a chimp hippocampus of 1.48 cm3,
flagged PROVISIONAL (sparse/lopsided QC) and sitting 30-50% below the allometric
line like the other propagated points. This script repeats the propagation with a
SECOND, independent macaque atlas -- CIVM (Calabrese et al. 2015, Duke; via the
Scalable Brain Atlas, template CBCetal15) -- onto the SAME chimpanzee scan, using
the SAME 1 mm affine pipeline as scripts/segment_primates.py (dipy MI,
translation->rigid->affine, reduced level_iters, nearest-neighbour label warp).

Hippocampus = CIVM label 79 ("Hip"), key found 2026-11-17 from the SBA's own
per-template key (outputs/civm_label_key_hunt.md; index2acr.json saved in
outputs/). Labels 143/158 are cortex (V4V/FST) and are NOT used.

Standing caveats: this is a foreign pipeline (Calabrese 2015) -- cross-check
material only, never pooled into the project's fits undeclared. Both this and the
D99 value are affine propagations, so agreement cannot exclude shared method bias.
Comparators: D99 propagation 1.48 cm3; modern stereology 1.77 cm3.
"""
import nibabel as nib, numpy as np, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nilearn import image as nimage
from scipy import ndimage
from dipy.align.imaffine import AffineRegistration, MutualInformationMetric, transform_centers_of_mass
from dipy.align.transforms import TranslationTransform3D, RigidTransform3D, AffineTransform3D

GOLD = os.path.expanduser("~/workspace/goldmine-hunter/gold/sba-macaque")
os.makedirs("outputs/segmentations", exist_ok=True)

def coarse(img, target=1.0, interp="continuous"):
    # Identical helper to scripts/segment_primates.py (fixed 2026-11-16 version).
    z = np.array(img.header.get_zooms()[:3], dtype=float)
    if z.mean() >= target * 0.999: return img
    f = float(z.mean() / target)
    aff = img.affine.copy(); aff[:3, :3] /= f
    shape = tuple(max(1, int(round(s * f))) for s in img.shape[:3])
    return nimage.resample_img(img, target_affine=aff, target_shape=shape, interpolation=interp)

# --- Static side: CIVM b0 template + hippocampus (label 79) ---
# Project convention (segment_primates.py / segment_felids.py): the ATLAS is the
# registration static, the SUBJECT is the moving image, and transform_inverse
# pulls the atlas labels into subject space. (A first run of this script flipped
# the assignment and produced a meaningless 0.18 cm3 on the template grid --
# discarded, see processing log 2026-11-17.)
b0 = nib.load(f"{GOLD}/civm_rhesus_v1_b0.nii.gz")
lab = nib.load(f"{GOLD}/civm_rhesus_v1_labels.nii.gz")
hip_full = nib.Nifti1Image((np.asanyarray(lab.dataobj) == 79).astype(np.uint8), lab.affine)
tmpl_c = coarse(b0)
hip_c = coarse(hip_full, interp="nearest")
static = np.asarray(tmpl_c.get_fdata(dtype=np.float32))
print(f"CIVM coarse static {tmpl_c.shape} zooms {[round(float(v),2) for v in tmpl_c.header.get_zooms()[:3]]}; "
      f"template hip vox (coarse) {int((np.asanyarray(hip_c.dataobj)>0).sum())}", flush=True)

# --- Moving side: chimpanzee MRI masked with the catalogue's own Atlas mask ---
subj = nib.load("data/brain_catalogue_full/Chimpanzee/MRI-n4.nii.gz")
mask = nib.load("data/brain_catalogue_full/Chimpanzee/Atlas.nii.gz")
d = np.squeeze(subj.get_fdata(dtype=np.float32)); m = np.squeeze(np.asanyarray(mask.dataobj)) > 0
masked = nib.Nifti1Image(d * m, subj.affine)
mov_c = coarse(masked)
moving = np.asarray(mov_c.get_fdata(dtype=np.float32))
print(f"Chimp coarse moving {mov_c.shape} zooms {[round(float(v),2) for v in mov_c.header.get_zooms()[:3]]}", flush=True)

# --- Affine registration, same recipe as the D99 run ---
affreg = AffineRegistration(metric=MutualInformationMetric(nbins=32), level_iters=[200, 100, 25], verbosity=0)
affine = transform_centers_of_mass(static, tmpl_c.affine, moving, mov_c.affine).affine
for tr in [TranslationTransform3D(), RigidTransform3D(), AffineTransform3D()]:
    reg = affreg.optimize(static, moving, tr, None, static_grid2world=tmpl_c.affine, moving_grid2world=mov_c.affine, starting_affine=affine)
    affine = reg.affine
    print(f"{tr.__class__.__name__} stage done", flush=True)

warped = reg.transform_inverse(np.asarray(hip_c.get_fdata(dtype=np.float32)), interpolation="nearest")
warped_bin = (warped > 0).astype(np.uint8)
nib.Nifti1Image(warped_bin, mov_c.affine).to_filename("outputs/segmentations/Chimpanzee_hippocampus_CIVM_propagated.nii.gz")
vox = float(np.prod(mov_c.header.get_zooms())) / 1000.0
vol = float(warped_bin.sum()) * vox
print(f"CIVM-propagated chimp hippocampus: {vol:.2f} cm3 ({int(warped_bin.sum())} vox @ {vox:.4f} cm3/vox)", flush=True)

# --- QC stats: components, bilateral split, centroid ---
cc, ncomp = ndimage.label(warped_bin)
sizes = ndimage.sum_labels(warped_bin, cc, range(1, ncomp + 1)) if ncomp else np.array([])
order = np.argsort(sizes)[::-1] if ncomp else []
print(f"components: {ncomp}; top sizes (vox): {[int(sizes[i]) for i in order[:6]]}", flush=True)
mid = warped_bin.shape[0] // 2
lv = float(warped_bin[:mid].sum()) * vox; rv = float(warped_bin[mid:].sum()) * vox
print(f"left/right split at grid midline x={mid}: {lv:.2f} / {rv:.2f} cm3", flush=True)
cen = ndimage.center_of_mass(warped_bin)
print(f"centroid (vox, coarse grid): {[round(float(c),1) for c in cen]} of shape {warped_bin.shape}", flush=True)

# --- QC figure: axial x3 + coronal + sagittal through the label mass ---
dd = moving  # chimp coarse image (the grid the warped label now lives on)
zs = [int(round(c)) for c in cen]
slices = []
for dz in (-4, 0, 4):
    k = min(max(zs[2] + dz, 0), dd.shape[2] - 1)
    slices.append(("axial", k))
slices.append(("coronal", min(max(zs[1], 0), dd.shape[1] - 1)))
slices.append(("sagittal", min(max(zs[0], 0), dd.shape[0] - 1)))
fig, axes = plt.subplots(1, 5, figsize=(15, 3.4))
for ax, (kind, idx) in zip(axes, slices):
    if kind == "axial": bg, ov = dd[:, :, idx], warped_bin[:, :, idx]
    elif kind == "coronal": bg, ov = dd[:, idx, :], warped_bin[:, idx, :]
    else: bg, ov = dd[idx, :, :], warped_bin[idx, :, :]
    ax.imshow(np.rot90(bg), cmap="gray")
    ax.imshow(np.ma.masked_where(np.rot90(ov) == 0, np.rot90(ov)), cmap="Reds", alpha=0.8, interpolation="nearest")
    ax.set_title(f"{kind} {idx}"); ax.axis("off")
fig.suptitle(f"Chimpanzee - CIVM-propagated hippocampus (label 79), {vol:.2f} cm3")
fig.tight_layout()
fig.savefig("outputs/segmentations/qc_chimpanzee_hippocampus_CIVM.png", dpi=130)
print("QC figure saved: outputs/segmentations/qc_chimpanzee_hippocampus_CIVM.png", flush=True)
