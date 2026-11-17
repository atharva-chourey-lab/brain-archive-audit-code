# Item 3 — Ferret residual forensics: FORM FAILURE (post-hoc)

**Status: POST-HOC in full**, per `PREDICTION.md` §5 — the residual
(+70.7%: label 0.173 cm³ vs 0.101 predicted at brain 6.13 cm³) was
registered unexplained; the forensic sequence was declared in advance in
`PREREGISTRATION_followups_2026-11-17.md` Item 3, which disciplines the
investigation but does not change its post-hoc status. Numbers:
`outputs/ferret_forensics_results.json`. No refitting.

## (a) Label integrity — CLEAN

- Header/affine **identical** to the MRI (200×384×160×1, 0.12 mm iso,
  RAS); no kangaroo-style corruption. Label = 100,257 vox = **0.1732 cm³**,
  reproducing the registered value.
- Components: 4; the top two hold 99.994% (50,467 / 49,784 vox); dust
  0.006% — negligible.
- **Per-side volumes** (split at the Otsu-mask centroid, ax0 = 98.7):
  **0.0872 vs 0.0860 cm³, ratio 0.986** — symmetric by volume, not merely
  by centroid. No sloth-bear one-sidedness, no giraffe unilaterality.
- Position **verified on overlays in three planes**
  (`outputs/dolphin_feasibility/ferret_qc.png`): coronal slices show the
  arch cut in its two classic positions per side (dorsal over the
  thalamus; ventral in the temporal lobe), sagittal slices show the two
  limbs of the arch. The label is in the right anatomy.
- One catalogue-semantics note: the ferret **Neocortex label overlaps
  67.3% of the hippocampus label's voxels**. The overlay shows why: the
  catalogue's "Neocortex" is the full cortical sheet, drawn straight over
  the medial wall without excluding the hippocampal formation. The
  overlap is a property of the neocortex label, not a misplacement of the
  hippocampus label (whose position is verified above). Declared, not
  pooled into any measurement.

## (b) Denominator — EXONERATED

The fit's 6.13 cm³ is an Otsu mask (no Atlas mask in the folder).
Recomputed Otsu band: **6.27 / 6.19 / 6.11 / 5.97 cm³** at ×0.8 / ×0.9 /
×1.0 / ×1.1 — tight and stable (no platypus-style whole-head failure).
Residual across the band: **+67.7% to +74.8%**. A zero residual would
require a brain of **11.55 cm³** (~12 g) — 1.85× the measured brain, and
no published ferret brain approaches it (Jardim-Messeder et al. 2017's
specimen: 3.097 g — which, if anything, would push the residual the
*other* way; the catalogue specimen at ~6.4 g is consistent with a large
male of a strongly dimorphic species, and with the Hutchinson template
population's size range). The denominator contributes at most a few
points.

## (c) Literature — the ferret runs high everywhere it is measured

- **Patzke et al. 2015 compilation carries no *Mustela putorius* row**
  (verified against the full Table 1; its only mustelid is *M. nivalis*).
  The least weasel (Reep primary, in `outputs/benchmark_testset.csv`):
  Vh 0.168 at Vb 2.068 → **+315.9% vs the registered line**, +19.6% vs
  Patzke's model. Same family, same direction, far larger.
- **Hutchinson et al. 2017** (population MRI/DTI templates of the adult
  ferret brain, *NeuroImage* 152:575–589; 26 in vivo + 8 ex vivo scans),
  as tabulated in a cross-species fractional-volume comparison: ferret
  hippocampus = **3.63% of brain volume** — *higher* than this specimen's
  2.83%. The independent MRI-class evidence says the catalogue ferret is,
  if anything, on the low side for its species. No absolute published
  ferret hippocampus volume in cm³ was found; the fractional value is
  what exists.

## (d) Form failure — the residual is the line's typical small-brain error

- The §3 benchmark's size-band medians for the registered line: 65.7%
  (<2 cm³), **69.0% (2–20 cm³)**, 51.3% (>20 cm³). The ferret's +70.7%
  sits essentially **at** the median error of its own size band — a
  typical miss for this functional form in this range, not an outlier.
- Patzke's saturating exponential at 6.13 cm³ predicts **0.333 cm³**; the
  ferret is **−48.0%** against it. The two models bracket the
  measurement (0.101 / 0.173 / 0.333): the power law's slope forces the
  hippocampal share down to 1.65% at 6.13 cm³, while measured small-brain
  shares run 2.8–3.6% (ferret, two MRI sources) and 8–11% below 2 cm³.
  A single power law cannot follow that bend (BENCHMARK.md's post-hoc
  diagnosis); the ferret, the smallest brain *inside* the n = 8 fit set,
  shows the strain in-sample.

## Verdict: FORM FAILURE

Not label artifact (integrity clean, position verified, independent MRI
share higher). Not denominator (band-tight; zero-residual brain size is
biologically absurd for the species). Not definition mismatch (no
broader-definition signature: the label matches the atlas parcellation's
anatomy and reads *low* against it). Not a genuine specimen residual:
its size is the line's demonstrated median error in the ferret's size
band, the comparator model built for this range deviates in the opposite
direction, and the only congeneric literature point deviates the same
way, harder. The +70.7% is the power-law form failing at the small end,
measured on one of its own fit points.

**What would refute this verdict:** an MRI-class hippocampus measurement
of another small mustelid (or a second ferret specimen) landing within
±25% of the registered line at a comparable brain size — that would make
the deviation specimen-specific (a genuine residual) rather than
form-driven.
