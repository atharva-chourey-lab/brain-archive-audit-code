# Item 1 — Dolphin hippocampus delineation: FAILED at QC (recorded, not rescued)

**Status: the delineation FAILED its registered QC gates. No hippocampus
volume is claimed for either dolphin specimen.** This file is the record of
the attempt, its numbers, and exactly what is missing. Protocol:
`PREREGISTRATION_followups_2026-11-17.md` Item 1 (committed `86c3636` before
any measurement). Run script: `scripts/delineate_bottlenose_hippocampus.py`.
Failed tracing retained, labelled: `outputs/segmentations/bottlenose_tracing_v1_FAILED.nii.gz`,
numbers in `outputs/dolphin_tracing_v1_FAILED_results.json`.

## What was done

**Calibration (passed).** In the bottlenose scan (Brain Catalogue,
`Bottlenose_dolphin/MRI-n4.nii.gz`, 0.301×0.301×0.300 mm; Atlas mask
515.46 cm³), the CSF system of the medial temporal wall — inferior horn +
hippocampal fissure + ambient cistern — segments cleanly as one connected
dark network per hemisphere at in-mask intensity < 100 (horn interior median
68; tissue ≥ ~140). Cross-check on the catalogue's own labels in the same
scan family: lion hippocampus label median intensity 191 (telencephalon
median 159), cat 111 (telencephalon 125) — hippocampal tissue reads in the
gray-matter band, so the dark network is CSF, not the formation. Montie et
al. 2007's boundary formulation (atlas, pp. 1471–1473) was verified from the
paper itself: inferior horn = lateral border, parahippocampal sulcus =
ventral border, subarachnoid space = medial/dorsal borders, the hippocampus
"located more central in the medial wall of the temporal lobes."

**Tracing v1.** Manual slice-by-slice polygons (ax1 128–192, step 4,
nearest-neighbour coverage 126–194; rostral/caudal limits per the
registration) around the bright rolled-lamina complex in the medial wall of
the inferior horn, mask = polygon ∩ Atlas ∩ (MRI ≥ 100).

**Tracing v1 numbers (the failed object's numbers — NOT a hippocampus
volume):** total 3.44 cm³ (side ax0<mid 1.83, side ax0≥mid 1.61); two main
components (67,390 / 59,195 vox) + dust 159 vox (0.13%); L/R ratio 0.88;
±1-voxel boundary sensitivity −24.8% / +14.6%.

## QC gate verdicts (registered gates, applied as written)

- (a) **FAIL.** Coronal overlays look plausible in isolation, but the
  sagittal overlay shows the mask as a rectangular slab cutting across the
  folded temporal cortex, and the axial overlay shows two wide blocks
  filling the medial temporal lobe between horn and midline. The traced
  object is the medial temporal cortical mass (parahippocampal/perirhinal
  cortex), not a lamina confined to the medial wall of the inferior horn —
  extension into temporal neocortex, which gate (a) forbids.
  (`outputs/dolphin_feasibility/qc_overlay_v1.png`.)
- (b) PASS — exactly two main components, dust 0.13% < 2%.
- (c) PASS — L/R 0.88, inside 0.5–2.0.
- (d) **FAIL.** 3.44 cm³ is outside the registered sanity band 0.3–2.0 cm³.
  Gate (d) re-inspection was performed: the anatomy does **not** genuinely
  read as a 3.44 cm³ hippocampus (see (a)); the value is therefore not
  reportable with a discrepancy declared — the delineation itself failed.
- (e) Reported above (moot under failure).

The registered expectation (own-denominator residual −70% to −95%) is
**neither confirmed nor refuted**: the test failed at the measurement
stage. The v1 object's residual (−20.4% vs the line at 515.46 cm³) is a
property of the wrong object and is not evidence about the cetacean
cluster.

## Why it failed — the boundary that does not exist in this specimen

Montie's tracing worked because in **in-situ T2** scans the hippocampus is
an island wrapped on all sides by CSF ("the fluid spaces around the
hippocampus in Figs. 5 and 6"). The Brain Catalogue specimen is an
**extracted, formalin-fixed** brain. In it, the dorsal/lateral CSF sheet
survives as a landmark, but the ventral and medial CSF borders are
collapsed: the formation is continuous with the parahippocampal cortex with
no cleft along most of its extent, and its internal lamina is not resolved
as a traceable boundary in this contrast (the internal lines visible in the
medial wall are the sulci of the surrounding gyri, as the sagittal QC
shows). Any tracing therefore either takes the whole medial temporal mass
(v1: 3.44 cm³, demonstrably neocortex-inclusive) or cuts an arbitrary
sub-band. Both are indefensible under the registered landmarks.

This is the published record's own conclusion for this specimen class,
stated before this build ran (Montie et al. 2007, *Anat. Rec.*
290:1471–1473): MRI studies of formalin-fixed cetacean brains "have been
unable to identify the hippocampus, except in the killer whale," the
bottlenose dolphin is named among the species in which it could not be
identified, and the mechanism given is exactly the one found here — loss of
the CSF spaces around the hippocampus on extraction, plus dorsal–ventral
thinning under the brain's weight.

## La Plata dolphin — attempted, same verdict

`La_Plata_dolphin/MRI.nii.gz` (0.25 mm iso; telencephalon label 91.29 cm³;
no whole-brain denominator exists). Inspection renders
(`outputs/dolphin_feasibility/laplata_*.png`): the ventromedial temporal
wall shows folded cortex and cisternal/vessel patterns but no
CSF-bounded lamina separable under the registered landmarks — the same
missing-boundary diagnosis, at a smaller absolute scale. **No delineation
attempted beyond inspection; no volume claimed.** (Placement via
Schwerdtfeger et al. 1984 was not reached and is moot.)

## What is missing (what would make this measurement possible)

1. A scan of a bottlenose (or other small odontocete) specimen in which the
   peri-hippocampal CSF spaces survive — in-situ T2/PD of the Montie type —
   or a T2-weighted scan of this specimen class with the ventral/medial
   clefts visible.
2. Or the Brain Catalogue team's own cetacean hippocampus delineation /
   protocol, if one is ever produced (both catalogue files are empty
   placeholders, nz = 0).
3. Or histological sections of this specimen.
4. Or a tracing by a cetacean neuroanatomist working from the primary
   literature's specimen-level knowledge.
   Note Montie's killer-whale exception (identifiable in fixed-brain MRI
   by absolute size): the catalogue holds no orca scan; a future attempt
   belongs there, not on the small delphinids.

**What would refute this failure verdict:** a delineation of this same
scan, under the registered landmarks, that passes gates (a)–(e) — i.e.
shows, in sagittal and axial overlay, a lamina confined to the medial wall
of the inferior horn without crossing temporal cortical folds, at a volume
inside 0.3–2.0 cm³.
