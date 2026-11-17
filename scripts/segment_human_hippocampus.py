"""Catalogue HUMAN hippocampus by atlas propagation (model-estimated, NOT manual):
Harvard-Oxford subcortical hippocampus labels (MNI152 space, local copy) warped into
the Brain Catalogue human specimen via dipy affine registration (mutual information).
Subject brain-masked first with the catalogue's own Atlas mask. QC overlay + volume
against the adult sanity band (~4-9 cm3 bilateral)."""
import nibabel as nib, numpy as np, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nilearn import datasets

os.makedirs("outputs/segmentations", exist_ok=True)
subj = nib.load("data/brain_catalogue_full/Human/MRI-n4.nii.gz")
atlas_mask = nib.load("data/brain_catalogue_full/Human/Atlas.nii.gz")
d = subj.get_fdata(dtype=np.float32); m = np.asanyarray(atlas_mask.dataobj) > 0
masked = nib.Nifti1Image(d * m, subj.affine)
masked.to_filename("outputs/segmentations/Human_brain_masked.nii.gz")

mni = datasets.load_mni152_template(resolution=1)
ho_img = nib.load("data/atlases/HarvardOxford/HarvardOxford-sub-maxprob-thr50-1mm.nii.gz")
import re
xml = open("data/atlases/HarvardOxford-Subcortical.xml").read()
# NOTE: this distribution's maxprob image values are XML index + 1 (verified anatomically:
# value 9/19 are the bilateral ~4.3k-voxel medial-temporal pair; value 8 is the brainstem).
hi = [int(v) + 1 for v, name in re.findall(r'<label index="(\d+)"[^>]*>([^<]*Hippocampus[^<]*)</label>', xml)]
print("HO hippocampus voxel values:", hi)
hip_mni = nib.Nifti1Image(np.isin(np.asanyarray(ho_img.dataobj), hi).astype(np.uint8), ho_img.affine)

from dipy.align.imaffine import AffineRegistration, MutualInformationMetric
from dipy.align.transforms import TranslationTransform3D, RigidTransform3D, AffineTransform3D
static = np.asarray(mni.get_fdata(dtype=np.float32))
moving = np.asarray(masked.get_fdata(dtype=np.float32))
affreg = AffineRegistration(metric=MutualInformationMetric(nbins=32), verbosity=0)
from dipy.align.imaffine import transform_centers_of_mass
affine = transform_centers_of_mass(static, mni.affine, moving, masked.affine).affine
for tr in [TranslationTransform3D(), RigidTransform3D(), AffineTransform3D()]:
    reg = affreg.optimize(static, moving, tr, None, static_grid2world=mni.affine, moving_grid2world=masked.affine, starting_affine=affine)
    affine = reg.affine
warped = reg.transform_inverse(np.asarray(hip_mni.get_fdata(dtype=np.float32)), interpolation="nearest")
nib.Nifti1Image(warped.astype(np.uint8), masked.affine).to_filename("outputs/segmentations/Human_hippocampus_propagated.nii.gz")
vox = float(np.prod(masked.header.get_zooms())) / 1000.0
print(f"Propagated hippocampus volume: {float((warped > 0).sum()) * vox:.2f} cm3 (sanity band 4-9)")
zz = int(np.argmax([(warped[:, :, k] > 0).sum() for k in range(warped.shape[2])]))
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(np.rot90(d[:, :, zz]), cmap="gray")
ax.imshow(np.ma.masked_where(np.rot90(warped[:, :, zz]) == 0, np.rot90(warped[:, :, zz])), cmap="Reds", alpha=0.75, interpolation="nearest")
ax.set_title(f"Catalogue human - propagated hippocampus overlay, z={zz}"); ax.axis("off")
fig.savefig("outputs/segmentations/qc_human_hippocampus.png", dpi=130)
print("QC figure saved")
