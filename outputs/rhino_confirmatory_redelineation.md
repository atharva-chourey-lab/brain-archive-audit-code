# Item 2 — Rhino confirmatory re-delineation: prediction REFUTED

**Registered test** of the fixed prediction in `REPORT.md` addendum
2026-11-17 §(f): re-delineating the catalogue black-rhino MRI under the
tight protocol T1–T7 (`PREREGISTRATION_followups_2026-11-17.md`, commit
`86c3636`) was predicted to give **≈4.2 cm³**. Run script:
`scripts/delineate_rhino_hippocampus_tight.py`. Mask:
`outputs/segmentations/rhino_hippocampus_tight_delineation.nii.gz`;
numbers: `outputs/rhino_tight_delineation_results.json`.

## Result

**Fresh tight delineation = 6.97 cm³** (hemispheres: ax0<mid **2.41**,
ax0≥mid **4.57** cm³; catalogue label: 2.431 / 4.424 — the label's
asymmetry reproduces under independent tracing, ratio 0.53). Span
ax1 142–190; two main components kept per T4; ±1-voxel boundary
sensitivity **−28.2% / +21.9%** (erode-1 = 5.01, dilate-1 = 8.50 cm³).
Dice vs the catalogue label 0.667 (same object, boundary-level
differences). QC overlays eyeballed in three planes
(`outputs/dolphin_feasibility/rhino_tight_qc.png`): the tracing forms the
arch — dorsal portion over the diencephalon, lateral rise, ventral
vertical portion — with no midline crossing and no spill into distant
cortex. Counting every traced voxel before the T4 main-component filter
gives 7.45 cm³ (the 0.48 cm³ difference is traced fragments disconnected
by polygon coarseness, mostly rostral ventral patches); the registered
primary number is the T4-filtered 6.97.

## Verdict: REFUTED (registered band ≥ 5.48 cm³)

An honest tight tracing reproduces the catalogue label, slightly
exceeding it (+1.7%). The verdict is robust to boundary placement: even
the erode-1 bound of the new tracing (5.01 cm³) stays above the CONFIRMED
band's ceiling (4.83). Reaching 4.2 would require shaving ~2 voxels off
every surface of the lamina band — a boundary the MRI does not show: the
band is bounded on both faces by dark CSF/fissure lines, and the tracing
follows those lines.

**Decomposition (why the prediction failed).** The declared exclusion
classes are tiny: rostral thread 0.031 + dust 0.074 ≈ **0.105 cm³ (1.5%
of the label)**. Label minus exclusions = 6.75 cm³; the fresh tracing of
the remainder = 6.97. There is no hidden ~2.6 cm³ excludable component in
the label: its bulk *is* the MRI-visible lamina band (dorsal oval +
ventral band + lateral column), and that band measures ~7 cm³ on this
scan under the tight criteria as registered.

## Consequences for the record

1. The rhino investigation's verdict (`outputs/rhino_investigation.md`,
   post-hoc) — "label artifact, delineation-definition class" — is **not
   confirmed by its own registered confirmatory test**. The
   definition-mismatch mechanism fails as operationalized here. The
   registered residual **reopens**: the catalogue rhino's hippocampus
   stands at **+83.5%** vs the registered line (tracing 6.97 vs predicted
   3.80 at brain 442.65 cm³), unexplained by denominator (exonerated),
   dust/thread (1.5%), boundary placement (±1 voxel cannot reach the
   band), or definition (this test).
2. The evidentiary picture inverts. Previously: Patzke histology 7.48 vs
   Bhagwandin MRI 4.71 (ratio 1.59×) made Bhagwandin the like-for-like
   anchor and the label the outlier. Now there are two MRI-class tracings
   of the band — the catalogue's (6.85) and this one (6.97) — agreeing
   with each other and sitting only 1.09× below the histology value,
   while Bhagwandin's 4.71 is the low outlier of the three. Declared
   candidate explanations, untested: (a) the specimens differ
   (Bhagwandin's brain 531 g vs catalogue 442.65 cm³; the "same specimen"
   inference from identical brain mass was always probabilistic, and it
   was Patzke's row, not the catalogue's, that matched that mass);
   (b) Bhagwandin's 2 mm T1-IR tracing under-measured a ~9.5 mm sheet
   (partial-volume thinning); (c) this specimen's hippocampus is
   genuinely large for the line.
3. Consequence for the registered line: none taken (no refitting,
   `PREDICTION.md` §6). The rhino remains a fit-set member with a large,
   now doubly-measured, unexplained positive residual.

**What would refute this REFUTED verdict:** an independent tracing of
this scan (human expert or sub-voxel method) landing ≤ 4.83 cm³ under
T1–T7; or specimen-level evidence (histology, a labelled rhino atlas)
that a named ~2 cm³ component of the bright band is not hippocampal
formation.
