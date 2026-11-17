"""Item 1 — Bottlenose dolphin hippocampus delineation (Brain Catalogue specimen).

Protocol: PREREGISTRATION_followups_2026-11-17.md, Item 1 (committed 86c3636
before measurement). Execution = manual slice-by-slice tracing of the rolled
lamina complex in the medial wall of the inferior horn, against Montie et al.
2007/2008 landmarks (inferior horn = lateral border, parahippocampal sulcus =
ventral border, subarachnoid space / hippocampal fissure = medial/dorsal
borders), on grid-labelled coronal renders (outputs/dolphin_feasibility/
trace_*.png). Polygons below were read off those renders by the tracer.

Declared execution details:
- Traced slices: ax1 = 128..192 step 4; each polygon covers, by nearest
  neighbour, ax1 in [y-2, y+1]; the last (192) extends to 194, the first
  (128) starts coverage at 126. Delineated span: ax1 126-194.
- Rostral limit: first slice where the lamina is separated from the
  amygdaloid complex by the horn's incursion = 128 (transitional head slices
  116-125 excluded under the registered rostral-limit rule; declared
  under-coverage of the head).
- Caudal limit: last slice where the formation is a coherent lamina in the
  medial wall of the inferior horn = 192 (at 196-204 the cross-section
  merges into the rising posterior temporal mass toward the trigone;
  excluded under the registered caudal-limit rule).
- Mask = polygon AND Atlas mask AND MRI >= 100 (the CSF threshold validated
  in calibration: horn interior median 68; tissue >= ~140).
- Sides: 'A' = ax0 < 224 (mask-centroid plane), 'B' = ax0 >= 224. Axcodes
  LPS: ax0 increases toward the subject's left, so B = subject's left.
- Uncertainty: +-1-voxel boundary sensitivity (erode/dilate, dilate
  restricted to Atlas mask AND MRI >= 100), per registered gate (e).
"""
import json
import nibabel as nib
import numpy as np
from scipy import ndimage
from matplotlib.path import Path

VOX_CM3 = 0.301 * 0.301 * 0.300 / 1000.0

# (ax0, ax2) vertices per traced slice, read from trace_*.png grid renders.
POLY = {
128: {'A': [(161,96),(178,98),(196,97),(202,92),(201,80),(196,72),(180,69),(166,71),(160,78),(159,88)],
      'B': [(283,95),(266,92),(252,90),(247,84),(248,76),(254,72),(268,70),(280,73),(284,82),(284,90)]},
132: {'A': [(157,94),(174,96),(194,95),(202,90),(200,79),(195,72),(181,69),(166,70),(158,77),(156,86)],
      'B': [(282,94),(264,96),(250,94),(246,87),(246,77),(253,71),(267,69),(279,72),(283,80),(283,88)]},
136: {'A': [(158,93),(176,95),(196,94),(202,89),(200,78),(194,71),(178,68),(164,70),(157,77),(156,85)],
      'B': [(284,93),(265,95),(252,92),(247,85),(248,76),(256,71),(270,70),(281,74),(284,82),(284,88)]},
140: {'A': [(155,92),(174,95),(194,94),(202,89),(200,77),(193,70),(177,67),(163,69),(155,76),(153,84)],
      'B': [(287,92),(268,94),(254,91),(248,84),(249,75),(257,70),(272,69),(283,73),(287,81),(287,87)]},
144: {'A': [(153,93),(172,96),(192,95),(201,90),(200,79),(194,71),(178,68),(163,69),(155,76),(153,85)],
      'B': [(289,93),(268,95),(254,92),(248,85),(249,76),(257,70),(270,69),(282,72),(288,79),(289,87)]},
148: {'A': [(153,92),(173,95),(193,94),(201,89),(199,79),(193,71),(178,68),(164,69),(156,76),(153,84)],
      'B': [(291,92),(270,95),(255,92),(249,85),(250,76),(258,71),(271,70),(283,73),(289,80),(290,86)]},
152: {'A': [(151,91),(171,95),(192,94),(201,89),(199,79),(193,71),(177,68),(162,69),(154,76),(151,84)],
      'B': [(291,92),(270,94),(255,91),(249,84),(250,75),(258,70),(271,69),(283,72),(289,79),(290,86)]},
156: {'A': [(150,90),(170,94),(191,94),(200,89),(199,79),(192,71),(176,68),(161,69),(153,76),(151,83)],
      'B': [(292,91),(270,94),(254,91),(248,84),(249,75),(257,70),(270,69),(282,72),(288,78),(290,85)]},
160: {'A': [(149,90),(170,94),(192,93),(201,88),(199,78),(192,70),(176,68),(161,69),(152,76),(150,83)],
      'B': [(292,89),(268,93),(253,90),(248,83),(249,75),(257,69),(270,68),(283,71),(290,77),(291,83)]},
164: {'A': [(149,89),(170,93),(192,93),(201,88),(199,78),(192,70),(176,68),(161,69),(152,76),(150,82)],
      'B': [(291,89),(268,92),(253,90),(248,83),(249,75),(257,69),(270,68),(282,71),(289,77),(290,83)]},
168: {'A': [(148,90),(169,94),(191,93),(200,88),(198,78),(191,70),(175,68),(160,69),(151,76),(149,83)],
      'B': [(292,90),(268,93),(253,90),(247,83),(248,75),(256,70),(269,69),(282,72),(289,78),(291,84)]},
172: {'A': [(147,91),(168,95),(190,94),(199,89),(197,79),(190,71),(174,69),(159,70),(150,77),(148,84)],
      'B': [(291,91),(267,94),(252,91),(247,84),(248,76),(256,71),(269,70),(281,73),(288,79),(290,85)]},
176: {'A': [(146,92),(168,96),(190,95),(200,90),(198,79),(191,71),(175,69),(159,70),(149,77),(147,84)],
      'B': [(297,93),(272,96),(256,93),(250,86),(251,77),(258,71),(271,70),(284,73),(293,79),(296,86)]},
180: {'A': [(146,93),(167,97),(189,96),(199,91),(197,80),(190,72),(174,70),(158,71),(149,78),(147,85)],
      'B': [(295,94),(270,97),(255,94),(250,87),(251,78),(258,72),(271,71),(283,74),(291,80),(294,87)]},
184: {'A': [(143,94),(165,98),(188,97),(198,92),(196,81),(189,73),(173,71),(157,72),(147,79),(145,86)],
      'B': [(299,95),(272,99),(256,96),(250,89),(251,80),(258,73),(271,71),(284,74),(293,81),(297,88)]},
188: {'A': [(141,96),(163,100),(186,99),(197,94),(195,83),(188,75),(172,73),(156,74),(146,81),(143,88)],
      'B': [(297,97),(270,101),(255,98),(249,90),(250,81),(257,74),(270,72),(283,75),(292,82),(295,89)]},
192: {'A': [(136,98),(158,102),(182,101),(198,95),(196,84),(188,77),(172,75),(155,76),(142,82),(137,90)],
      'B': [(299,99),(272,102),(258,98),(252,90),(253,81),(260,75),(274,74),(288,77),(296,84),(298,92)]},
}

base = 'data/brain_catalogue_full/Bottlenose_dolphin/'
img = nib.load(base + 'MRI-n4.nii.gz')
mri = img.get_fdata()
atlas = nib.load(base + 'Atlas.nii.gz').get_fdata() > 0
tissue = atlas & (mri >= 100)

traced = sorted(POLY.keys())
assign = {}
for y in range(126, 195):
    assign[y] = min(traced, key=lambda t: (abs(t - y), t))

mask = np.zeros(mri.shape, dtype=bool)
xx, zz = np.meshgrid(np.arange(mri.shape[0]), np.arange(mri.shape[2]), indexing='ij')
pts = np.stack([xx.ravel(), zz.ravel()], axis=1)
for y, t in assign.items():
    for side in ('A', 'B'):
        path = Path(POLY[t][side])
        inside = path.contains_points(pts).reshape(mri.shape[0], mri.shape[2])
        sl = inside & tissue[:, y, :]
        mask[:, y, :] |= sl

def vol(m):
    return float(m.sum() * VOX_CM3)

lab, n = ndimage.label(mask)
sizes = ndimage.sum_labels(mask, lab, range(1, n + 1)) if n else []
order = np.argsort(sizes)[::-1] if n else []
main = np.zeros_like(mask)
for o in order[:2]:
    main |= lab == o + 1
dust_vox = int(mask.sum() - main.sum())
res = {'voxel_cm3': VOX_CM3, 'span_ax1': [126, 194],
       'components_total': int(n),
       'component_sizes_vox': [int(s) for s in sorted(sizes, reverse=True)][:6],
       'dust_vox': dust_vox}
for side, sl in [('A_ax0_lt_mid', slice(0, 224)), ('B_ax0_ge_mid', slice(224, None))]:
    m = main.copy(); m2 = np.zeros_like(mask); m2[sl] = True
    res[side + '_cm3'] = vol(main & m2)
res['total_cm3'] = vol(main)
res['dust_frac'] = dust_vox / max(int(mask.sum()), 1)
res['LR_ratio_B_over_A'] = res['B_ax0_ge_mid_cm3'] / res['A_ax0_lt_mid_cm3']
ero = ndimage.binary_erosion(main)
dil = ndimage.binary_dilation(main) & tissue
res['erode1_cm3'] = vol(ero)
res['dilate1_cm3'] = vol(dil)
res['minus1vox_pct'] = 100 * (res['erode1_cm3'] - res['total_cm3']) / res['total_cm3']
res['plus1vox_pct'] = 100 * (res['dilate1_cm3'] - res['total_cm3']) / res['total_cm3']
pred_own = 10 ** (-1.6609 + 0.8467 * np.log10(515.46))
pred_typ = 10 ** (-1.6609 + 0.8467 * np.log10(1476.83))
res['line_pred_own_denom_cm3'] = float(pred_own)
res['residual_own_denom_pct'] = 100 * (res['total_cm3'] - pred_own) / pred_own
res['line_pred_species_typical_cm3'] = float(pred_typ)
res['residual_species_typical_pct'] = 100 * (res['total_cm3'] - pred_typ) / pred_typ
print(json.dumps(res, indent=1))

import os
os.makedirs('outputs/segmentations', exist_ok=True)
out = nib.Nifti1Image(main.astype(np.uint8), img.affine, img.header)
out.set_data_dtype(np.uint8)
nib.save(out, 'outputs/segmentations/bottlenose_hippocampus_delineation.nii.gz')
np.save('outputs/segmentations/bottlenose_main_mask.npy', main)
with open('outputs/dolphin_delineation_results.json', 'w') as f:
    json.dump(res, f, indent=1)
print('saved mask + results')
