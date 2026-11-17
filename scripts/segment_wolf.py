"""GRAY WOLF hippocampus by D99 macaque-atlas propagation — a deliberate long shot:
cross-ORDER (primate atlas -> carnivore), on a scan already flagged for poor contrast
and a bright artefact region. Expected outcome is an honest QC failure; the overlay
is the judge. Differences from segment_primates.py: wolf file is MRI.nii.gz (not
MRI-n4), and there is no catalogue Atlas mask, so the brain mask is Otsu + fill +
largest component (the lion volumetry recipe). Allometric expectation ~0.78 cm3
(slope-0.81 line at the wolf's ~57.7 cm3 brain); plausibility band 0.3-1.5 cm3."""
import nibabel as nib, numpy as np, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nilearn import image as nimage
from dipy.align.imaffine import AffineRegistration, MutualInformationMetric, transform_centers_of_mass
from dipy.align.transforms import TranslationTransform3D, RigidTransform3D, AffineTransform3D
from skimage.filters import threshold_otsu
from scipy import ndimage as ndi

HIPP = [317, 386, 488, 489, 352, 381, 455, 487, 490]
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

sp = "Gray_wolf"
subj = nib.load(f"data/brain_catalogue_full/{sp}/MRI.nii.gz")
d = np.squeeze(subj.get_fdata(dtype=np.float32))
thr = threshold_otsu(d[d > 0])
m = ndi.binary_fill_holes(d > thr)
lab, n = ndi.label(m)
if n > 1:
    sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
    m = lab == (1 + int(np.argmax(sizes)))
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
warped = reg.transform_inverse(np.asarray(hip_c.get_fdata(dtype=np.float32)), interpolation="nearest")
nib.Nifti1Image(warped.astype(np.uint8), mov_c.affine).to_filename("outputs/segmentations/Gray_wolf_hippocampus_propagated.nii.gz")
vox = float(np.prod(mov_c.header.get_zooms())) / 1000.0
vol = float((warped > 0).sum()) * vox
print(f"{sp}: propagated hippocampus {vol:.2f} cm3 (plausibility band 0.3-1.5; allometric expectation ~0.78)", flush=True)
dd = np.asarray(mov_c.get_fdata(dtype=np.float32))
zz = int(np.argmax([(warped[:, :, k] > 0).sum() for k in range(warped.shape[2])]))
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(np.rot90(dd[:, :, zz]), cmap="gray")
ax.imshow(np.ma.masked_where(np.rot90(warped[:, :, zz]) == 0, np.rot90(warped[:, :, zz])), cmap="Reds", alpha=0.75, interpolation="nearest")
ax.set_title(f"Gray wolf - D99-propagated hippocampus overlay, z={zz}"); ax.axis("off")
fig.savefig("outputs/segmentations/qc_gray_wolf_hippocampus.png", dpi=130)
print(f"{sp}: QC figure saved", flush=True)
