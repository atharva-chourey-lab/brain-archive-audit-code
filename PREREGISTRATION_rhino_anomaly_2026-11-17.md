# Pre-registration — Rhino anomaly investigation (five directions)

**Registered: 2026-11-17 (late evening), commissioned by Atharva the same day.**
The git commit carrying this file is the registration record. It is written
*before* any of the five tests below is run. Project rules carry over
(`PREDICTION.md` §6): no refitting of the registered line; missing = missing,
never zero; method classes never pooled undeclared; failed/void tests recorded
as failed/void. Nothing public.

## State of the record this registration starts from

- Registered line (fixed ruler, never refitted):
  `log10(Vh) = −1.6609 + 0.8467 × log10(Vb)`, n = 8, r = 0.930.
- Catalogue black-rhino specimen: brain (Atlas mask) **442.65 cm³**; line
  prediction at that volume **3.80 cm³**.
- Hippocampus, MRI class, same specimen, two tracings: catalogue label
  **6.854 cm³** (+80.5% vs line, registered in `PREDICTION.md` §5); fresh
  tight re-delineation under T1–T7 **6.97 cm³** (+83.5%), `REPORT.md`
  addendum (h). The pre-fixed ≈4.2 cm³ confirmatory prediction was REFUTED;
  the delineation-definition verdict of addendum (e) is superseded.
- Literature: Patzke et al. 2015 compilation (histology class) *Diceros
  bicornis* **7.48 cm³** at Vb 512.55 (Mb 531 g); Bhagwandin, Haagensen &
  Manger 2017 MRI volumetry **4.71 cm³** on a black rhino of brain mass
  531 g, and 3.97 cm³ on a white rhino of 536.5 g.
- The residual stands **reopened and unexplained**: denominator exonerated,
  dust/thread 1.5%, boundary placement (±1 voxel) cannot reach the line,
  definition mechanism refuted by its own registered test.

**Question.** Is there a mechanism — specimen, structure profile, sampling
method, or ruler — that accounts for a doubly-measured MRI hippocampus of
≈6.9 cm³ in a 442.65 cm³ black-rhino brain? Five attacks, each with verdict
rules fixed here. Anything improvised during the run is labelled post-hoc
in the output, per project custom.

---

## Direction 1 — Specimen identity

**Why.** This catalogue has documented metadata corruption (red-kangaroo
label header copied from the sloth-bear files, `PREDICTION.md` §1; red
squirrel "Hippocampus" file duplicating its whole-brain mask, REPORT.md
2026-11-16 addendum). If the rhino scan is not what its folder name claims,
the anomaly is a filing error.

**Evidence chain to assemble (all of it, in this order):**
1. The Brain Catalogue species page for the rhino (braincatalogue.org):
   species name as printed, any specimen metadata (sex, age, source,
   institution), and the full list of files offered.
2. Zenodo: presence or absence of a rhinoceros record in the Brain
   Catalogue's Zenodo deposits (the 2016 set, records 44790–44866, contains
   no rhino; the local files came from the website, 2026-11-17).
3. The original source publication for the scan, if the page or record
   names one (the catalogue's scans derive from Santin, Herbin & Toro's
   collection and named contributors).
4. Internal consistency: mask volume 442.65 cm³ (mass-equivalent ≈458.6 g
   at the compilation's 1.036 g/cm³) against the published black-rhino
   brain masses (531 g, Patzke row and Bhagwandin specimen; white rhino
   536.5 g). Declared in advance: the two rhino species' masses overlap, so
   mass cannot separate species; and catalogue specimens run small against
   endocast volumes (lion: mask 188.1 vs endocranial mean 244.4), so a
   volume deficit alone cannot refute identity either. Volume bears only
   on the narrower question "same individual as the 531 g specimen."

**Verdict rules (fixed):**
- **CONFIRMED** — a documented chain (page/record/source paper) names the
  species *Diceros bicornis* for this scan with no contradicting link.
- **DOUBTFUL** — a chain exists but the specimen is unnamed/unsourced at
  one or more links, so identity rests on the folder label alone.
- **REFUTED** — the documented chain names a different species or a
  specimen inconsistent with this scan, or the page itself attributes the
  scan elsewhere.
- Separately, and regardless of the above: the claim "same individual as
  the Patzke/Bhagwandin 531 g specimen" is graded **unlikely** if the
  mass-equivalent deficit (458.6 vs 531 g, −13.6%) exceeds what the
  catalogue's own specimen-vs-literature pattern shows for the lion
  (mask/endocast = 0.77, i.e. deficits of this size occur), in which case
  it is graded **not excludable on volume alone** and left to the
  documentary chain. (Declared now so the number cannot be argued either
  way after the fact: 0.864 sits inside the lion's 0.77–1.0 pattern band,
  so volume will NOT be used to refute same-specimen identity; only
  documents can.)

**What would refute the surviving hypothesis:** if identity is CONFIRMED,
a primary source (contributor record, source paper's specimen table)
naming a different species or specimen for this scan file.

## Direction 2 — Whole-brain profile of the same specimen

**Why.** A hippocampus can be extreme because the *specimen* is unusual
(everything shifted) or because the *structure* is extreme in an otherwise
ordinary brain. These have opposite meanings.

**Measurements (fixed):** every label openly listed for this specimen on
the catalogue species page as of the run date, downloaded under the
catalogue's CC BY-NC 4.0 terms (data stay gitignored, per project policy),
plus the Atlas mask already held. For each label: volume, share of the
Atlas-mask brain volume, component census, and a position overlay eyeball
(the project's standard QC). The hippocampus numbers are already in the
record and are not re-measured here except as the profile's anchor row.

**References (fixed, declared per structure before measuring):** a
structure's residual is computed only where a reference exists in a
declared class:
- Hippocampus: the registered line and Patzke's model (Direction 5).
- Any other structure: Bhagwandin et al. 2017's same-species MRI volumetry
  table (black rhino), if the paper reports that structure — method class
  MRI, same species, different specimen (declared). Share-vs-share
  comparison (this specimen's share vs their specimen's share) is the
  primary form, since the specimens differ in brain size.
- If the paper reports no value for a structure, that structure is
  profiled by share alone and marked **no reference** — never compared
  across method classes undeclared.

**MRI-class share table (fixed):** hippocampal share (Vh/Vb) for all 14
catalogue species carrying a hippocampus value in
`outputs/cross_species_volumes_v3.csv` (10 direct labels + 4
model-estimated propagations), each row flagged with its data class;
artifact-flagged labels (sloth bear — one-sided; giraffe — unilateral)
marked, not silently dropped. The rhino's rank is reported (i) among the
10 direct labels and (ii) among direct labels with brain > 100 cm³.

**Verdict rules (fixed):**
- **STRUCTURE STORY** — hippocampus extreme (per Direction 5) while every
  other referenced structure's share sits within ±35% of its same-species
  MRI reference.
- **SPECIMEN STORY** — at least half of the other referenced structures
  deviate from their references in the *same direction* by > 35%.
- **MIXED** — anything between.
- **INSUFFICIENT** — fewer than two other structures carry a reference;
  the profile is then reported descriptively and no story verdict is
  claimed.

**What would refute the surviving hypothesis:** for a STRUCTURE verdict,
a same-species MRI reference set showing the other structures equally
shifted; for a SPECIMEN verdict, references showing them ordinary.

## Direction 3 — Second-specimen hunt

**Why.** One specimen cannot carry a species claim. If any other
rhinoceros brain MRI is openly downloadable, it outranks every argument
in this document.

**Search protocol (fixed — every cell must be filled for a NONE verdict):**
1. Brain Catalogue: full species census re-checked for any rhinoceros
   (black, white, Indian, Javan, Sumatran) beyond the held specimen.
2. Zenodo: queries "rhinoceros brain", "Diceros", "Ceratotherium",
   "Rhinoceros unicornis" (MRI/neuroimaging records).
3. MorphoSource, OpenNeuro, NITRC: same taxon queries (declared in
   advance: MorphoSource is predominantly CT; a CT endocast is NOT an MRI
   and would be logged as found-but-wrong-modality, not measured).
4. Literature: Manger-lab and other rhinoceros neuroanatomy publications
   after Bhagwandin et al. 2017 that report new MRI data or deposit scans;
   plus any "rhinoceros brain MRI atlas" claim.
5. General web: the same taxon + "brain MRI" / "brain scan download"
   queries.

**Verdict rules (fixed):**
- **FOUND + OPEN** — a scan is downloadable without a gate: delineate its
  hippocampus under T1–T7 (the registered tight protocol of
  `PREREGISTRATION_followups_2026-11-17.md`, Item 2) and report the value
  with the same QC gates; placement vs the registered line at its own
  denominator.
- **FOUND + GATED** — exists but behind agreement/paywall: name it,
  measure nothing.
- **NONE OPENLY AVAILABLE** — licensed only with the full search log
  (queries, repositories, dates, hits) in the output document.

**What would refute a NONE verdict:** anyone producing an openly
downloadable rhinoceros brain MRI outside the held specimen.

## Direction 4 — Bhagwandin reconciliation: simulate their method on our mask

**Why.** Bhagwandin et al. 2017's 4.71 cm³ is the low outlier of the three
rhino values. If their sampling/estimation scheme, applied to our traced
mask, returns ≈4.71, the gap is an estimator artifact and the anomaly
shrinks to "our specimen vs the line." If it returns ≈7, their 4.71 is a
property of their specimen or their tracing, not of the estimator.

**Method extraction (fixed):** from the full text of Bhagwandin,
Haagensen & Manger 2017 (*Front. Neuroanat.* 11:74; open access,
PMC5583206), extract verbatim-supported facts: scanner/sequence, slice
thickness and interval, tracing plane and software, whether every slice
was traced or every k-th, the volume estimator (voxel count vs Cavalieri
area×interval), and the stated hippocampal inclusion boundaries and
specimen data. Anything the paper does not state is recorded as
**not stated** — never filled in from convention.

**Simulation (fixed; primary on the tight mask
`outputs/segmentations/rhino_hippocampus_tight_delineation.nii.gz`,
secondary on the catalogue label):**
- If the paper's scheme is **Cavalieri subsampling** at interval *k*
  sections (or physical interval *d* mm): compute the mask's coronal
  cross-sectional area series (axis 1, the tracing plane of T6), subsample
  at that interval at **every phase offset**, volume = Σ areas × interval;
  report min/median/max across phases.
- If the scheme is **voxel counting on thick slices**: partial-volume
  simulation — average the binary mask into slabs of the paper's slice
  thickness along axis 1, threshold at 0.5 (declared proxy for a tracer
  calling a voxel in/out), count; across every phase offset; report
  min/median/max.
- If the paper states **both** a thick acquisition and full tracing, the
  thick-slice branch is primary. If it states neither interval nor
  thickness computably, the direction is graded **NOT COMPUTABLE AS
  STATED** and the closest declared proxy (2 mm slabs, per the candidate
  mechanism named in addendum (h)) is run and labelled post-hoc.
- The same simulation is run at a ladder of intervals around the stated
  one (×0.5, ×1, ×2) as a declared sensitivity, so a near-miss is visible
  as a near-miss.

**Verdict rules (fixed), against the target 4.71 cm³:**
- **METHOD EXPLAINS THE GAP** — the phase-median simulated volume falls
  within ±10% of 4.71 (4.24–5.18) at the paper's stated scheme.
- **PARTIAL** — the simulated distribution reaches 4.71 only at extreme
  phases, or the phase-median closes ≥ 50% of the 6.97 → 4.71 gap without
  landing in the band.
- **FAILS** — phase-median simulated volume ≥ 5.5 cm³: the estimator, as
  stated, cannot turn this mask into 4.71.

**What would refute the surviving hypothesis:** if METHOD EXPLAINS, a
re-simulation under the paper's verbatim scheme (e.g. their true tracing
axis, if not coronal) landing ≥ 5.5; if FAILS, documentary evidence that
their tracing excluded a named component our T1–T7 includes (that would
move the gap to Direction 2's definition territory, already refuted for
*our* label — it would then be a claim about *their* tracing, testable
only on their scan, which is not open).

## Direction 5 — Line-side robustness: restate the anomaly at surviving strength

**Why.** +83.5% is measured against the registered line, which is (a) fit
on n = 8 with the rhino *in* the fit set, and (b) known to fail as a form
(the §3 benchmark). An anomaly that exists only against a broken ruler is
a property of the ruler.

**Computations (fixed):**
- (a) Rhino residual vs **Patzke et al. 2015's saturating exponential**,
  as published and as transcribed in `scripts/benchmark.py`:
  `ln(Vh) = 9.26 × (0.72 − exp(−0.097 × ln(Vb)))`. Computed for: the
  tracing (6.97) and the label (6.854) at Vb 442.65; and, as the model's
  own-specimen check, the compilation's 7.48 at Vb 512.55.
- (b) **MRI-class standing:** signed residuals vs the registered line for
  all 14 v3 hippocampus points, printed with class flags (fit member /
  artifact-flagged label / model-estimated — never pooled silently);
  rhino's rank by signed residual among the 10 direct labels; rhino's
  share rank (from Direction 2).
- (c) A declared sensitivity: the residual of the rhino against the
  registered line refitted *without* the rhino (leave-one-out, n = 7) —
  computed and printed as a sensitivity only; the registered line itself
  is not moved (§6), and the LOO number is labelled exploratory.

**Restatement rule (fixed):** the anomaly is claimed at the **weakest**
formulation that survives all three computations:
- If the rhino is the largest positive direct-label residual AND its
  share ranks top-2 among large-brain (>100 cm³) direct labels AND its
  residual vs Patzke's model is ≥ +30%: the anomaly stands as
  **"extreme inside its own method class by every ruler available."**
- If any leg fails, the claim is restated at exactly the strength the
  surviving legs support (e.g. "largest share among large-brain MRI
  labels, but within Patzke-model scatter"), naming the failed leg.
- The +83.5% figure may be quoted only with its in-sample caveat attached.

**What would refute the surviving hypothesis:** a same-class (MRI)
hippocampus measurement set in which the rhino's share/residual is
unremarkable — i.e. the Direction 3 second specimen landing on the line,
or a wider MRI label census reclassifying the share table.

---

## Outputs (fixed)

- `outputs/rhino_anomaly_investigation.md` — the full record: per
  direction, verdict + numbers + refutation condition.
- `outputs/rhino_anomaly_results.json` — machine-readable numbers.
- `REPORT.md` — new dated addendum (k), appended; body and addenda
  (a)–(i) untouched.
- `logs/processing_log.md` — closing entry.
- Local commits only. Nothing public.
