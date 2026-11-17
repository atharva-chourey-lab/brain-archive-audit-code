#!/usr/bin/env python3
"""Rhino anomaly investigation — Direction 4: simulate Bhagwandin et al.
2017's sampling scheme on our traced rhino hippocampus mask.

Pre-registered in PREREGISTRATION_rhino_anomaly_2026-11-17.md (commit
e53edfd). Method facts extracted verbatim from the paper (PMC5583206):

  - Acquisition: T1-weighted inversion recovery, "2 mm slices without gap"
    (Methods, MRI section). Scanned in coronal, sagittal, horizontal planes.
  - Volumetry: NO estimator, interval, tracing plane, tracer or software
    stated in the paper; calculation delegated by citation to "the
    methodology of Patzke et al. (2015)". OsiriX named for image processing.
  - Figure captions: displayed coronal sections are 2 mm thick and 6 mm
    apart (a display subset; the paper never states volumetry used it).

Per the registration's fallback: the verbatim scheme is NOT COMPUTABLE AS
STATED (no estimator). The closest declared proxy is primary here and is
labelled as a proxy: contiguous 2 mm slabs along the coronal axis (axis 1,
the project's tracing plane and the paper's figured plane), binary mask
averaged within each slab, threshold 0.5, voxel-count x slab thickness,
across every phase offset. Declared secondaries: Cavalieri subsampling of
the coronal area series at 6 mm (the figure-display spacing) and at 2 mm
(sanity); slab ladder at 1 mm and 4 mm (x0.5 / x2 sensitivity). A threshold
sweep (0.25 / 0.75) is POST-HOC and labelled as such.

Target: Bhagwandin et al.'s black-rhino hippocampus = 4.71 cm3.
Registered verdict bands (against the primary proxy): phase-median within
4.24-5.18 -> METHOD EXPLAINS; median closes >=50% of the 6.97->4.71 gap or
4.71 reached only at extreme phases -> PARTIAL; median >= 5.5 -> FAILS.
"""
import json

import nibabel as nib
import numpy as np

VOX = 0.045  # cm (0.45 mm isotropic)
TARGET = 4.71
FULL = 6.97  # tight tracing total (T4-filtered), outputs/rhino_tight_delineation_results.json


def slab_sim(mask, thick_mm, thresh=0.5):
    """Average binary mask into contiguous slabs of thick_mm along axis 1,
    threshold, count. Returns volume (cm3) for every phase offset."""
    step = thick_mm / 0.45
    n = mask.shape[1]
    out = []
    phase = 0.0
    while phase < step:
        # slab boundaries in voxel units, starting at -phase
        edges = np.arange(-phase, n + step, step)
        vol_vox = 0.0
        for lo, hi in zip(edges[:-1], edges[1:]):
            lo_i, hi_i = int(np.ceil(lo)), int(np.floor(hi))
            lo_i, hi_i = max(lo_i, 0), min(hi_i, n)
            if hi_i <= lo_i:
                continue
            frac = mask[:, lo_i:hi_i, :].mean(axis=1)  # per-voxel-column mean
            vol_vox += float((frac >= thresh).sum()) * (hi - lo)
        # vol_vox is a voxel count (columns x slab width in voxels);
        # one voxel = 0.45^3 mm3 = 9.1125e-5 cm3.
        out.append(vol_vox * 9.1125e-05)
        phase += 0.45  # shift by one native slice
    return out


def cavalieri(areas_cm2, interval_mm):
    """Subsample a per-slice (0.45 mm) area series at interval_mm, all
    phases (0.45 mm steps), volume = interval x sum of sampled areas."""
    step_vox = interval_mm / 0.45
    out = []
    off = 0.0
    pos_all = np.arange(len(areas_cm2)) * 0.45  # mm positions of slice centres
    while off < interval_mm:
        pos = off + np.arange(0, pos_all[-1] + 1e-9, interval_mm)
        a = np.interp(pos, pos_all, areas_cm2)
        out.append(float(a.sum() * (interval_mm / 10.0)))
        off += 0.45
    return out


def stats(vals):
    v = np.asarray(vals, float)
    return {"min": round(float(v.min()), 3), "median": round(float(np.median(v)), 3),
            "max": round(float(v.max()), 3), "n_phases": int(len(v))}


def main():
    def load3(path):
        d = nib.load(path).get_fdata()
        if d.ndim == 4:  # catalogue files carry a trailing singleton dim
            assert d.shape[3] == 1
            d = d[..., 0]
        return d > 0

    tight = load3("outputs/segmentations/rhino_hippocampus_tight_delineation.nii.gz")
    label = load3("data/brain_catalogue_full/Black_rhinoceros/Hippocampus.nii.gz")
    res = {"target_bhagwandin_cm3": TARGET, "full_tight_cm3": FULL,
           "full_label_cm3": round(float(label.sum()) * 9.1125e-05, 3)}

    for name, mask in (("tight", tight), ("label", label)):
        areas = mask.sum(axis=(0, 2)) * (0.045 ** 2)  # cm2 per 0.45 mm slice
        res[name] = {
            "slab_2mm_primary_PROXY": stats(slab_sim(mask, 2.0)),
            "slab_1mm_ladder": stats(slab_sim(mask, 1.0)),
            "slab_4mm_ladder": stats(slab_sim(mask, 4.0)),
            "cavalieri_6mm_figure_spacing": stats(cavalieri(areas, 6.0)),
            "cavalieri_2mm_sanity": stats(cavalieri(areas, 2.0)),
            "slab_2mm_thresh0.25_POSTHOC": stats(slab_sim(mask, 2.0, 0.25)),
            "slab_2mm_thresh0.75_POSTHOC": stats(slab_sim(mask, 2.0, 0.75)),
        }

    med = res["tight"]["slab_2mm_primary_PROXY"]["median"]
    gap_closed = (FULL - med) / (FULL - TARGET)
    if 4.24 <= med <= 5.18:
        verdict = "METHOD EXPLAINS THE GAP (against the declared 2 mm proxy)"
    elif med >= 5.5 and gap_closed < 0.5:
        verdict = "FAILS (against the declared 2 mm proxy)"
    else:
        verdict = "PARTIAL (against the declared 2 mm proxy)"
    res["verdict_primary_proxy"] = {
        "phase_median_2mm_slab_tight": med,
        "fraction_of_gap_closed_by_median": round(float(gap_closed), 3),
        "verdict": verdict,
        "scheme_status": "Bhagwandin et al. state no estimator; verbatim scheme "
                         "NOT COMPUTABLE AS STATED. Verdict graded against the "
                         "declared proxy (2 mm contiguous slabs, threshold 0.5).",
    }
    with open("outputs/rhino_anomaly_direction4.json", "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
