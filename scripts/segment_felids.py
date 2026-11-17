"""FELID RECONCILIATION — TEST A (PREDICTION.md §4): formation-level propagation.

Catalogue MRI hippocampus labels read ~2.2x below Reep, Finlay & Darlington
(2007) histology in both felids (lion 2.022 vs 4.496 cm3; leopard 1.178 vs
3.121). Question: is the gap delineation (catalogue pen drawn tight, missing
formation components) or does it sit on the histology side?

Test A propagates the FULL D99 hippocampal-formation union (CA1/CA2/CA3/CA4,
fascia dentata, subiculum, prosubiculum, presubiculum, parasubiculum — the
Reep/Stephan boundary content) onto the lion and leopard catalogue MRIs with
the established 1 mm affine MI pipeline (segment_primates.py / segment_wolf.py;
downsampler factor = z/target, the fixed version). Lion moving image masked
with its Otsu brain mask (outputs/lion_brainmask_otsu.npy, lion volumetry
recipe); leopard masked with its catalogue Atlas mask. Model-estimated, NOT
manual. Declared instrument caveat: affine propagation ran 24-43% BELOW the
allometric line on primate targets but +1.4% on the wolf — a lower-bound-
leaning instrument. The overlay is the judge: bilateral? medial-temporal?
sparse? Volumes are read off the ~1 mm warped grid, as in prior runs.
"""
import nibabel as nib, numpy as np, os, csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nilearn import image as nimage
from dipy.align.imaffine import AffineRegistration, MutualInformationMetric, transform_centers_of_mass
from dipy.align.transforms import TranslationTransform3D, RigidTransform3D, AffineTransform3D
from scipy import ndimage as ndi

HIPP = [317, 386, 488, 489, 352, 381, 455, 487, 490]  # verified vs D99_v2.0_labels_semicolon.txt
os.makedirs("outputs/segmentations", exist_ok=True)
d99t = nib.load("data/atlases/D99_v2.0_dist/D99_template.nii.gz")
d99a = nib.load("data/atlases/D99_v2.0_dist/D99_atlas_v2.0.nii.gz")
hip = nib.Nifti1Image(np.isin(np.asanyarray(d99a.dataobj), HIPP).astype(np.uint8), d99a.affine)

def coarse(img, target=1.0, interp="continuous"):
    z = np.array(img.header.get_zooms()[:3], dtype=float)
    if z.mean() >= target * 0.999: return img
    f = float(z.mean() / target)
    aff = img.affine.copy(); aff[:3, :3] /= f
    shape = tuple(max(1, int(round(s * f))) for s in img.shape[:3])
    return nimage.resample_img(img, target_affine=aff, target_shape=shape, interpolation=interp)

tmpl_c = coarse(d99t); hip_c = coarse(hip, interp="nearest")
static = np.asarray(tmpl_c.get_fdata(dtype=np.float32))

TARGETS = [
    # (name, mri path, mask kind)
    ("Lion", "data/lion/MRI-n4.nii.gz", "otsu_npy"),
    ("Leopard", "data/brain_catalogue_full/Leopard/MRI-n4.nii.gz", "atlas_file"),
]
rows = []
for sp, mri_path, mask_kind in TARGETS:
    subj = nib.load(mri_path)
    d = np.squeeze(subj.get_fdata(dtype=np.float32))
    if mask_kind == "otsu_npy":
        m = np.load("outputs/lion_brainmask_otsu.npy") > 0
        assert m.shape == d.shape, f"lion brain mask shape {m.shape} != MRI {d.shape}"
    else:
        m = np.squeeze(np.asanyarray(nib.load("data/brain_catalogue_full/Leopard/Atlas.nii.gz").dataobj)) > 0
    masked = nib.Nifti1Image(d * m, subj.affine)
    mov_c = coarse(masked)
    moving = np.asarray(mov_c.get_fdata(dtype=np.float32))
    print(f"{sp}: coarse moving {mov_c.shape} zooms {[round(float(v),2) for v in mov_c.header.get_zooms()[:3]]}; static {tmpl_c.shape}", flush=True)
    affreg = AffineRegistration(metric=MutualInformationMetric(nbins=32), level_iters=[200, 100, 25], verbosity=0)
    affine = transform_centers_of_mass(static, tmpl_c.affine, moving, mov_c.affine).affine
    for tr in [TranslationTransform3D(), RigidTransform3D(), AffineTransform3D()]:
        reg = affreg.optimize(static, moving, tr, None, static_grid2world=tmpl_c.affine, moving_grid2world=mov_c.affine, starting_affine=affine)
        affine = reg.affine
        print(f"{sp}: {tr.__class__.__name__} stage done", flush=True)
    warped = (reg.transform_inverse(np.asarray(hip_c.get_fdata(dtype=np.float32)), interpolation="nearest") > 0)
    nib.Nifti1Image(warped.astype(np.uint8), mov_c.affine).to_filename(f"outputs/segmentations/{sp}_hippocampus_D99formation_propagated.nii.gz")
    vox = float(np.prod(mov_c.header.get_zooms())) / 1000.0
    vol = float(warped.sum()) * vox
    # bilaterality: split at the brain mask's axis-0 centre of mass (coarse grid)
    mc = coarse(nib.Nifti1Image(m.astype(np.uint8), subj.affine), interp="nearest")
    mm = np.asarray(mc.get_fdata()) > 0
    mid = float(ndi.center_of_mass(mm)[0])
    left = float(warped[:int(round(mid))].sum()); right = float(warped[int(round(mid)):].sum())
    lab, ncomp = ndi.label(warped)
    sizes = np.sort(ndi.sum(np.ones_like(lab), lab, range(1, ncomp + 1)))[::-1] if ncomp else np.array([])
    top2 = float(sizes[:2].sum() / sizes.sum()) if ncomp else 0.0
    print(f"{sp}: propagated formation {vol:.3f} cm3 | components {ncomp}, top-2 share {top2:.2f} | L/R split at x={mid:.1f}: {left:.0f} / {right:.0f} vox", flush=True)
    rows.append(dict(species=sp, test="A_propagation", volume_cm3=round(vol, 3),
                     components=int(ncomp), top2_share=round(top2, 3),
                     left_vox=int(left), right_vox=int(right)))
    # QC overlay: coronal (axis-1 slice with most label) + axial, like prior QC sheets
    dd = moving
    yc = int(np.argmax([warped[:, k, :].sum() for k in range(warped.shape[1])]))
    za = int(np.argmax([warped[:, :, k].sum() for k in range(warped.shape[2])]))
    fig, axs = plt.subplots(1, 2, figsize=(11, 5.5))
    axs[0].imshow(np.rot90(dd[:, yc, :]), cmap="gray")
    axs[0].imshow(np.ma.masked_where(np.rot90(warped[:, yc, :]) == 0, np.rot90(warped[:, yc, :])), cmap="Reds", alpha=0.75, interpolation="nearest")
    axs[0].set_title(f"{sp} — coronal y={yc}"); axs[0].axis("off")
    axs[1].imshow(np.rot90(dd[:, :, za]), cmap="gray")
    axs[1].imshow(np.ma.masked_where(np.rot90(warped[:, :, za]) == 0, np.rot90(warped[:, :, za])), cmap="Reds", alpha=0.75, interpolation="nearest")
    axs[1].set_title(f"{sp} — axial z={za}"); axs[1].axis("off")
    fig.suptitle(f"{sp} — D99-formation propagated hippocampus (Test A)")
    fig.savefig(f"outputs/segmentations/qc_{sp.lower()}_D99formation.png", dpi=130)
    print(f"{sp}: QC figure saved (coronal y={yc}, axial z={za})", flush=True)

with open("outputs/felid_reconciliation_testA.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("wrote outputs/felid_reconciliation_testA.csv", flush=True)
