"""RED-NECKED WALLABY hippocampus by WITHIN-FAMILY propagation: the red kangaroo's
REAL catalogue hippocampus label (same family, Macropodidae) warped from the
kangaroo MRI onto the wallaby MRI (affine, dipy MI). Purpose: the kangaroo is the
v3 set's only marsupial and sits -49% below the placental line — a second
macropod point tests whether that is a clade deviation or one odd label.
Allometric expectation at the wallaby's 14.72 cm3 brain: ~0.24 cm3; the kangaroo's
own deviation would predict ~0.12 cm3. Class: model-estimated, flagged."""
import nibabel as nib, numpy as np, os, glob, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nilearn import image as nimage
from dipy.align.imaffine import AffineRegistration, MutualInformationMetric, transform_centers_of_mass
from dipy.align.transforms import TranslationTransform3D, RigidTransform3D, AffineTransform3D

os.makedirs("outputs/segmentations", exist_ok=True)

def coarse(img, target=1.0, interp="continuous"):
    z = np.array(img.header.get_zooms()[:3], dtype=float)
    if z.mean() >= target * 0.999: return img
    f = float(z.mean() / target)
    aff = img.affine.copy(); aff[:3, :3] /= f
    shape = tuple(max(1, int(round(s * f))) for s in img.shape[:3])
    return nimage.resample_img(img, target_affine=aff, target_shape=shape, interpolation=interp)

def masked_mri(sp):
    base = f"data/brain_catalogue_full/{sp}"
    mri_p = sorted(glob.glob(f"{base}/MRI*.nii.gz"))[0]
    subj = nib.load(mri_p)
    d = np.squeeze(subj.get_fdata(dtype=np.float32))
    mask_p = f"{base}/Atlas.nii.gz"
    if os.path.exists(mask_p):
        m = np.squeeze(np.asanyarray(nib.load(mask_p).dataobj)) > 0
        d = d * m
    return nib.Nifti1Image(d, subj.affine)

tmpl = masked_mri("Red_kangaroo")
hip_im = nib.load("data/brain_catalogue_full/Red_kangaroo/Hippocampus.nii.gz")
hip = nib.Nifti1Image((np.squeeze(np.asanyarray(hip_im.dataobj)) > 0).astype(np.uint8), hip_im.affine)
tmpl_c = coarse(tmpl); hip_c = coarse(hip, interp="nearest")
static = np.asarray(tmpl_c.get_fdata(dtype=np.float32))

mov_c = coarse(masked_mri("Red-necked_wallaby"))
moving = np.asarray(mov_c.get_fdata(dtype=np.float32))
print(f"Wallaby: coarse moving {mov_c.shape}; static (kangaroo) {tmpl_c.shape}", flush=True)
affreg = AffineRegistration(metric=MutualInformationMetric(nbins=32), level_iters=[200, 100, 25], verbosity=0)
affine = transform_centers_of_mass(static, tmpl_c.affine, moving, mov_c.affine).affine
for tr in [TranslationTransform3D(), RigidTransform3D(), AffineTransform3D()]:
    reg = affreg.optimize(static, moving, tr, None, static_grid2world=tmpl_c.affine, moving_grid2world=mov_c.affine, starting_affine=affine)
    affine = reg.affine
    print(f"Wallaby: {tr.__class__.__name__} stage done", flush=True)
warped = reg.transform_inverse(np.asarray(hip_c.get_fdata(dtype=np.float32)), interpolation="nearest")
nib.Nifti1Image(warped.astype(np.uint8), mov_c.affine).to_filename("outputs/segmentations/Red-necked_wallaby_hippocampus_propagated.nii.gz")
vox = float(np.prod(mov_c.header.get_zooms())) / 1000.0
vol = float((warped > 0).sum()) * vox
print(f"Wallaby: propagated hippocampus {vol:.2f} cm3 (line expectation ~0.24; kangaroo-rate expectation ~0.12)", flush=True)
dd = np.asarray(mov_c.get_fdata(dtype=np.float32))
zz = int(np.argmax([(warped[:, :, k] > 0).sum() for k in range(warped.shape[2])]))
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(np.rot90(dd[:, :, zz]), cmap="gray")
ax.imshow(np.ma.masked_where(np.rot90(warped[:, :, zz]) == 0, np.rot90(warped[:, :, zz])), cmap="Reds", alpha=0.75, interpolation="nearest")
ax.set_title(f"Red-necked wallaby - kangaroo-propagated hippocampus overlay, z={zz}"); ax.axis("off")
fig.savefig("outputs/segmentations/qc_red-necked_wallaby_hippocampus.png", dpi=130)
print("Wallaby: QC figure saved", flush=True)
