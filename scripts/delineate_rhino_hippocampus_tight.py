#!/usr/bin/env python
"""Item 2 - Rhino confirmatory re-delineation under the registered tight
criteria T1-T7 (PREREGISTRATION_followups_2026-11-17.md, commit 86c3636).

Fresh manual tracing from the MRI (NOT an erosion of the catalogue label):
the arch cross-section (dorsal oval over the diencephalon + ventral band
under the thalamus + lateral column, per T5) traced slice-by-slice in the
coronal plane on renders WITHOUT the label, following the dark CSF/fissure
lines that bound the lamina band on both faces. Ventral polygons are
restricted to the lateral segments (the midline ventral band is
fornix/hypothalamic tissue, not formation). Span ax1 142-190 (traced
144-188 step 4, NN coverage +-2): the rostral thread (ax1<140, T3) and the
caudal thread/dust (ax1>192, T4) are excluded classes. Search region per
T6 = label bbox dilated 2 (non-binding; polygons lie inside it).
Polygons read from outputs/dolphin_feasibility/rhino_trace_{a,b}.png.
"""
import json
import nibabel as nib
import numpy as np
from matplotlib.path import Path
from scipy import ndimage

BASE = 'data/brain_catalogue_full/Black_rhinoceros/'
VOX_CM3 = 0.45 ** 3 / 1000.0
MID = 132  # hemisphere split plane (Atlas centroid ax0 ~131.7)

# (ax0, ax2) polygons per traced slice; 'd'=dorsal oval, 'v'=ventral band,
# 'c'=lateral column / merged caudal cross-section, 't'=tail oval
POLYS = {
    144: {'Ld': [(63,110),(70,122),(78,131),(90,132),(96,124),(94,112),(85,106),(71,106),(64,108)],
          'Rd': [(169,109),(177,121),(186,130),(199,131),(206,123),(204,111),(193,105),(179,105),(171,107)],
          'Rv': [(152,62),(166,59),(176,63),(173,72),(158,74),(151,68)]},
    148: {'Ld': [(62,110),(70,123),(79,132),(91,133),(97,125),(95,112),(86,106),(71,106),(63,108)],
          'Rd': [(168,109),(177,122),(187,131),(200,132),(207,124),(205,111),(194,105),(179,105),(170,107)],
          'Lv': [(97,63),(108,60),(117,63),(115,72),(103,74),(96,69)],
          'Rv': [(150,62),(164,59),(177,62),(179,70),(168,76),(154,75),(149,68)]},
    152: {'Ld': [(60,108),(68,122),(77,132),(90,134),(99,127),(100,113),(92,104),(74,102),(63,104)],
          'Rd': [(166,107),(175,121),(185,131),(199,133),(208,126),(207,112),(197,103),(180,102),(169,104)],
          'Lv': [(92,62),(106,58),(120,59),(118,71),(100,74),(93,69)],
          'Rv': [(148,61),(160,58),(176,59),(184,64),(180,73),(164,77),(150,71)]},
    156: {'Ld': [(59,107),(67,121),(77,132),(91,134),(100,127),(101,112),(93,103),(74,101),(62,103)],
          'Rd': [(165,106),(174,120),(185,131),(200,133),(209,125),(208,111),(197,102),(179,101),(168,103)],
          'Lv': [(88,61),(104,57),(120,57),(118,70),(98,73),(90,69)],
          'Rv': [(147,60),(159,56),(179,57),(188,62),(184,72),(165,77),(149,71)]},
    160: {'Ld': [(58,106),(66,120),(76,132),(92,135),(102,127),(103,111),(94,102),(73,100),(61,102)],
          'Lc': [(60,78),(72,74),(76,84),(74,100),(66,104),(59,96),(58,84)],
          'Lv': [(86,60),(104,56),(120,56),(118,69),(98,73),(88,67)],
          'Rd': [(164,105),(173,119),(184,131),(201,133),(210,124),(209,110),(197,101),(178,100),(167,102)],
          'Rc': [(192,76),(203,74),(207,84),(205,100),(197,104),(191,94),(190,83)],
          'Rv': [(148,59),(158,55),(180,56),(190,61),(186,71),(166,77),(150,70)]},
    164: {'Ld': [(57,105),(65,119),(76,132),(93,135),(103,126),(104,110),(94,101),(72,99),(60,101)],
          'Lc': [(58,74),(71,71),(75,82),(73,100),(64,103),(57,94),(56,82)],
          'Lv': [(84,59),(103,55),(120,55),(118,68),(97,72),(86,66)],
          'Rd': [(163,104),(172,118),(184,131),(202,133),(211,123),(210,109),(197,100),(177,99),(166,101)],
          'Rc': [(191,73),(204,71),(208,82),(206,99),(197,103),(190,92),(189,81)],
          'Rv': [(147,58),(157,54),(181,55),(192,60),(188,70),(166,76),(149,69)]},
    168: {'Ld': [(57,104),(65,118),(76,131),(93,134),(103,125),(104,109),(94,100),(72,98),(60,100)],
          'Lc': [(57,72),(70,69),(74,81),(72,99),(63,102),(56,92),(55,80)],
          'Lv': [(83,58),(102,54),(120,54),(118,67),(96,71),(85,65)],
          'Rd': [(163,103),(172,117),(184,130),(202,132),(211,122),(210,108),(197,99),(177,98),(166,100)],
          'Rc': [(190,71),(204,69),(208,80),(206,98),(197,102),(189,90),(188,79)],
          'Rv': [(147,57),(156,53),(182,54),(193,59),(189,69),(166,75),(149,68)]},
    172: {'Ld': [(58,103),(66,116),(76,128),(91,131),(100,123),(100,108),(91,99),(73,98),(61,100)],
          'Lc': [(58,70),(70,67),(74,79),(72,97),(64,100),(57,90),(56,78)],
          'Lv': [(84,57),(102,53),(120,53),(118,66),(96,70),(86,64)],
          'Rd': [(164,102),(173,115),(184,128),(200,130),(208,121),(207,107),(196,98),(178,97),(167,99)],
          'Rc': [(189,69),(202,67),(206,78),(204,96),(196,100),(188,88),(187,77)],
          'Rv': [(147,56),(156,52),(180,53),(190,58),(186,68),(165,74),(149,67)]},
    176: {'Lc': [(60,64),(72,60),(78,72),(76,96),(80,112),(84,124),(76,130),(64,128),(58,112),(56,84),(56,70)],
          'Ld': [(76,100),(88,96),(96,104),(94,118),(84,124),(75,116),(73,106)],
          'Rc': [(176,62),(190,59),(198,68),(200,84),(196,100),(188,110),(180,104),(174,88),(173,72)],
          'Rd': [(168,98),(182,95),(192,100),(194,112),(188,122),(176,118),(168,108)]},
    180: {'Lc': [(62,62),(74,59),(80,70),(78,94),(82,108),(88,118),(80,126),(68,124),(60,108),(58,80),(59,68)],
          'Ld': [(80,96),(92,93),(99,100),(97,112),(88,119),(79,110),(77,102)],
          'Rc': [(174,60),(188,57),(196,66),(198,82),(194,98),(186,106),(178,100),(172,84),(171,70)],
          'Rd': [(166,94),(179,91),(189,96),(191,108),(184,117),(174,111),(166,102)]},
    184: {'Lt': [(64,66),(74,62),(84,68),(88,80),(86,96),(78,104),(68,100),(62,84),(62,72)],
          'Rt': [(176,64),(188,60),(200,66),(205,78),(202,94),(192,103),(181,99),(175,82),(174,71)]},
    188: {'Lt': [(66,68),(75,65),(83,70),(86,81),(84,94),(77,100),(69,96),(65,82),(64,73)],
          'Rt': [(178,66),(189,62),(199,67),(203,78),(200,91),(191,98),(182,94),(177,80),(176,72)]},
}

def main():
    img = nib.load(BASE + 'MRI-n4.nii.gz')
    mri = img.get_fdata().squeeze()
    atlas = nib.load(BASE + 'Atlas.nii.gz').get_fdata().squeeze() > 0
    lab = nib.load(BASE + 'Hippocampus.nii.gz').get_fdata().squeeze() > 0
    search = ndimage.binary_dilation(lab, iterations=2)
    shape = mri.shape
    mask = np.zeros(shape, dtype=bool)
    gx, gz = np.meshgrid(np.arange(shape[0]), np.arange(shape[2]), indexing='ij')
    pts = np.column_stack([gx.ravel(), gz.ravel()])
    for y, parts in POLYS.items():
        sl = np.zeros(shape[0] * shape[2], dtype=bool)
        for poly in parts.values():
            sl |= Path(np.array(poly, dtype=float)).contains_points(pts)
        sl = sl.reshape(shape[0], shape[2])
        for yy in range(y - 2, y + 2):
            if 0 <= yy < shape[1]:
                mask[:, yy, :] |= sl
    mask &= search & atlas
    # keep the two main components (T4 applied to the new tracing)
    lab_arr, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lab_arr, range(1, n + 1))
    order = np.argsort(sizes)[::-1]
    main_mask = np.isin(lab_arr, [order[0] + 1, order[1] + 1])
    dust = int(mask.sum() - main_mask.sum())
    L = main_mask[:MID]; R = main_mask[MID:]
    ero = ndimage.binary_erosion(main_mask)
    dil = ndimage.binary_dilation(main_mask) & atlas
    res = {
        'voxel_cm3': VOX_CM3,
        'span_ax1': [142, 190],
        'components_total': int(n),
        'dust_vox': dust,
        'dust_frac': dust / max(int(mask.sum()), 1),
        'L_ax0_lt_mid_cm3': float(L.sum() * VOX_CM3),
        'R_ax0_ge_mid_cm3': float(R.sum() * VOX_CM3),
        'total_cm3': float(main_mask.sum() * VOX_CM3),
        'erode1_cm3': float(ero.sum() * VOX_CM3),
        'dilate1_cm3': float(dil.sum() * VOX_CM3),
        'label_cm3': float(lab.sum() * VOX_CM3),
        'dice_vs_label': float(2 * (main_mask & lab).sum() / (main_mask.sum() + lab.sum())),
        'residual_vs_line_pct': float((main_mask.sum() * VOX_CM3 / 3.80 - 1) * 100),
    }
    res['minus1vox_pct'] = (res['erode1_cm3'] / res['total_cm3'] - 1) * 100
    res['plus1vox_pct'] = (res['dilate1_cm3'] / res['total_cm3'] - 1) * 100
    print(json.dumps(res, indent=1))
    nib.save(nib.Nifti1Image(main_mask.astype(np.uint8), img.affine),
             'outputs/segmentations/rhino_hippocampus_tight_delineation.nii.gz')
    np.save('outputs/segmentations/rhino_tight_main_mask.npy', main_mask)
    with open('outputs/rhino_tight_delineation_results.json', 'w') as f:
        json.dump(res, f, indent=1)
    print('saved mask + results')

if __name__ == '__main__':
    main()
