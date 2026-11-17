# Black rhinoceros hippocampus — anomaly investigation (five directions)

**Run:** 2026-11-17 (late evening) · **Pre-registered:**
`PREREGISTRATION_rhino_anomaly_2026-11-17.md` (commit `e53edfd`), written
before any of the five tests was run. Verdict rules below are the registered
ones, applied as written; improvisations are labelled post-hoc where they
occur. **Scripts:** `scripts/rhino_anomaly_direction5.py`,
`scripts/rhino_anomaly_direction4.py`. **Numbers:**
`outputs/rhino_anomaly_results.json`,
`outputs/rhino_anomaly_mri_class_table.csv`,
`outputs/rhino_anomaly_direction4.json`,
`outputs/rhino_anomaly_direction5.json`. No refitting. Nothing public.

## Bottom line

**No mechanism was found. The anomaly survives all five attacks** — and the
investigation changes what the anomaly *is*: it is now known to be a
property of **this specimen** (identity confirmed, and documented to be a
different animal from the ordinary Manger-lab rhino), it is **not** an
artifact of Bhagwandin et al.'s sampling (their estimator, under every
computable proxy, cannot turn a ≈7 cm³ mask into 4.71), and it stands at a
restated, defensible strength: **the largest hippocampal share of any valid
large-brain MRI label (1.548%), ≈+50% above Patzke's saturating model —
a level Patzke's own histology value for the species also reaches — with
the one MRI specimen that sits on the line (Bhagwandin's) now documented
as a different, larger-brained individual whose hippocampal share (0.919%)
is ordinary.** Surviving hypotheses, in the order the evidence leaves them:
(1) genuine elevation — this species, and this individual at its high end;
(2) a non-formation component inside the MRI-visible lamina band specific
to rhino anatomy, namable only with rhino histology that does not openly
exist; (3) an individual anomaly of a single specimen — untestable while
the world's open supply of rhino brain MRI is exactly this one scan.

---

## Direction 1 — Specimen identity: CONFIRMED (species); a different animal from the Manger specimen (documented)

**The chain, link by link:**

1. **Zenodo record 44797** — "Magnetic Resonance Imaging Scan of a Black
   Rhinoceros (Diceros Bicornis)", DOI 10.5281/zenodo.44797, published
   2016-01-15, creators Santin, Herbin & Toro, CC BY-NC 4.0, description
   pointing at braincatalogue.org/Black_rhinoceros. Its file,
   `MRI-n4.nii.gz` (9,457,983 bytes, md5 `fca0fc0b4fd328e92e3b6f080c120e92`),
   is **byte-identical to the local file** (md5 verified in this run).
   The companion mesh deposit is record 44795. *This corrects a premise
   in the project record:* the rhino was inside the catalogue's Zenodo
   deposit family all along (44795/44797); `data/brain_catalogue/
   PROVENANCE.md` enumerated only the morphospace downloads, and the
   "website-only" framing of the 2026-11-17 addendum reflects that
   enumeration gap, not the deposit's absence. A secondary works-listing
   of a 2016 rhino-scan title (found by the research pass) resolves to
   this record.
2. **Species page** (braincatalogue.org/Black_rhinoceros): heading "Black
   Rhinoceros (*Diceros Bicornis*)"; the only specimen-relevant text is
   the Acknowledgements — Marc Herbin (curator, Vertebrate Brain
   Collection, Jardin des Plantes, Paris) and Mathieu Santin (ICM/CENIR,
   Paris). Project-level provenance (NITRC mirror) matches: specimens from
   Herbin's collection, scanned at ICM by Santin/Petiet.
3. **File internals:** all three NIfTI files carry only the descrip
   "FreeSurfer May 25 2011" — no specimen identifiers embedded.
4. **No source publication describes this specimen.** The catalogue's
   journal paper (Heuer et al. 2019) is primates-only; an ISMRM 2020
   abstract covers the collection without rhino-specific metadata.

**What the chain does not contain:** sex, age, individual ID, acquisition
date. Individual identity is a blank, and is recorded as a blank.

**Not the Manger animal — now documented, not inferred.** Bhagwandin
et al. 2017's black rhino is a named individual: 40-year-old male,
National Zoological Gardens, Pretoria; perfusion-fixed, scanned at Wits
on a Philips 1.5 T with 2 mm slices; brain mass 531 g. The catalogue
specimen is a Paris museum-collection brain scanned at 0.45 mm isotropic;
its mask mass-equivalent is 458.6 g (−13.6%). Different collection,
different institution, different protocol, different size. The earlier
record's "same specimen" inference was always Patzke-row ↔ Bhagwandin
(both Manger lab, identical 531 g — confirmed again in this run against
the Patzke full text: *Diceros bicornis* Mb 531.00, Vb 512.55, Vh 7.48,
source code 5, the authors' own study). The catalogue specimen was never
that animal, and now the record can say so from documents.

**Verdict (registered rules): CONFIRMED** — the documented chain names
*Diceros bicornis* for this scan at every link, with a checksum-verified
file, and no contradicting link exists. The metadata-swap failure mode
(kangaroo/sloth-bear, red squirrel) does **not** apply here: the deposit
predates the website download by nine years and agrees with it exactly.

**What would refute it:** a primary source (contributor record, specimen
table) naming a different species for record 44797's file. None was found
in the chain, the deposit, or the collection literature.

## Direction 2 — Whole-brain profile: INSUFFICIENT (registered rule); descriptive profile reported

**The registered measurement set cannot be extended:** the catalogue
offers exactly two labels for this specimen — the Atlas whole-brain mask
and the Hippocampus label (site inventory and Zenodo deposit family
agree). Bhagwandin et al. 2017 *do* publish same-species MRI references
for three further structures — cerebellum 37.73 cm³, amygdala 3.10 cm³,
ventricular system 9.86 cm³ (all on their 512.55 cm³ specimen) — but no
catalogue labels exist for those structures in our specimen, so no
like-for-like share can be computed. Referenced other structures: **0**,
below the registered minimum of 2. **Verdict: INSUFFICIENT** — no
specimen-story/structure-story verdict is claimed. (A gyrification-index
comparison — Bhagwandin report GI 2.47 — was considered and not run: GI
is not in the registered measurement set, and an exposed-surface
computation from the mesh would be an improvised instrument.)

**Descriptive profile (all that the labels license):**

| Quantity | Catalogue specimen | Bhagwandin specimen (reference) |
|---|---|---|
| Brain volume | 442.65 cm³ (Atlas mask) | 512.55 cm³ (from 531 g) |
| Hippocampus share — label | **1.548%** | — |
| Hippocampus share — tight tracing | **1.575%** | — |
| Hippocampus share — their MRI tracing | — | **0.919%** (4.71 cm³) |
| Atlas mask extents (L–R × A–P × S–I) | 11.38 × 14.08 × 6.34 cm | not comparably published |

In share space the anomaly is a between-specimen fact: the only other
MRI-measured black rhino carries an ordinary hippocampal share; this
specimen carries one ≈1.7× larger. n = 1 against n = 1 — declared, not
pooled.

**MRI-class share table** (hippocampal share, all 14 catalogue species
carrying a hippocampus value; full table with residuals in
`outputs/rhino_anomaly_mri_class_table.csv`): the rhino's 1.548% ranks
**3rd of 14**, behind the ferret (2.822%, a 6.13 cm³ brain — the size band
where the line's form is registered to fail, addendum (i)) and the sloth
bear (2.714%, a label registered as an artifact — both components on one
side of the midline). Among **direct labels with brain > 100 cm³** the
rhino ranks **2nd of 5 counting the artifact, 1st of 4 among valid
labels** (lion 1.075%, panda 0.586%, giraffe 0.472% — the giraffe label
is itself unilateral-flagged).

**What would refute the descriptive profile:** catalogue labels for
further structures of this specimen, or a same-species MRI reference set,
showing the specimen's other structures equally shifted (specimen story)
or ordinary (structure story). Neither exists openly today (Direction 3).

## Direction 3 — Second-specimen hunt: NONE OPENLY AVAILABLE (checked claim)

Full protocol executed 2026-11-17; every registered cell filled:

| Cell | Result |
|---|---|
| Brain Catalogue census (37 species) | One rhinoceros only — the held specimen |
| Zenodo (web index **and direct API query** in this run) | The held specimen's own deposits (44797 MRI, 44795 mesh); all other hits taxonomic/genetic, no neuroimaging |
| MorphoSource | Rhinoceros holdings are long bones (Gravibone) and CT material; downloads account-gated; no brain MRI |
| OpenNeuro | No rhinoceros dataset (the 2025 Animal Brain Collection covers 29 mostly small amniotes, no rhino) |
| NITRC | Only the Brain Catalogue project mirror — the same Paris specimen |
| Post-2017 literature | Bhagwandin 2017 remains the last primary rhino MRI paper; its scans were **never deposited** (figures/values only). Iurino et al. 2020 report CT endocasts of *D. bicornis* and *C. simum* — CT, excluded by the registered protocol |
| General web | Funnels to the same three sources; a Sketchfab "Rhino Brain" mesh is a derivative of the held specimen; the ZARD zoo-radiology database is gated and CT-based |

**Verdict: NONE OPENLY AVAILABLE.** The world's open supply of rhinoceros
brain MRI is one specimen. The only other rhino brain MRIs known to exist
(Bhagwandin black + white, Wits) survive as printed values, not data.

*Declared limitation:* MorphoSource and OpenNeuro were searched through
the web index rather than their native internal search (no live-browser
operator in this run); Zenodo — the repository where a catalogue-family
deposit would live — was settled by direct API query. **What would refute
this verdict:** anyone producing an openly downloadable rhinoceros brain
MRI beyond the held specimen.

## Direction 4 — Bhagwandin reconciliation: FAILS — the estimator cannot produce 4.71 from this mask

**Verbatim method extraction** (Bhagwandin, Haagensen & Manger 2017,
*Front. Neuroanat.* 11:74, full text read): the paper's Volumetrics
section is one paragraph that **delegates every calculation by citation**
— hippocampus and amygdala "the methodology of Patzke et al. (2015)". It
states **no estimator, no sampling interval, no tracing plane, no tracer,
no volumetry software** (OsiriX is named for image processing). What it
does state verbatim: T1-weighted inversion recovery, **"2 mm slices
without gap"**, brains scanned in coronal, sagittal and horizontal
planes, Philips 1.5 T Intera. Its figure captions display coronal sections
"6 mm apart" — a display subset the paper never connects to the
volumetry. **The verbatim scheme is therefore NOT COMPUTABLE AS STATED**,
and per the registration the verdict is graded against the closest
declared proxy, labelled as such.

**Simulation** (`scripts/rhino_anomaly_direction4.py`; primary mask = the
T1–T7 tight tracing, 6.97 cm³; coronal axis; every phase offset):

| Scheme | min | phase-median | max |
|---|---|---|---|
| **2 mm contiguous slabs, threshold 0.5 (primary proxy)** | 7.07 | **7.21** | 7.31 |
| 1 mm slabs (ladder ×0.5) | 7.07 | 7.17 | 7.19 |
| 4 mm slabs (ladder ×2) | 6.96 | 7.30 | 7.52 |
| Cavalieri, 6 mm interval (figure spacing) | 6.72 | 6.92 | 7.28 |
| Cavalieri, 2 mm (sanity) | 6.88 | 6.92 | 7.07 |
| 2 mm slabs, threshold 0.75 (**post-hoc**) | 5.84 | 6.07 | 6.37 |
| 2 mm slabs, threshold 0.25 (**post-hoc**) | 8.01 | 8.29 | 8.57 |

The catalogue label under the primary proxy: median 6.76 (same picture).

**Reading.** Partial-volume averaging at their slice thickness does not
thin this structure — at the neutral threshold it slightly *fattens* it
(the lamina is ≈9.5 mm thick against 2 mm slices; it is not a
partial-volume-marginal object). The primary proxy's phase-median closes
**−10.5%** of the 6.97 → 4.71 gap, i.e. it widens it. Even the post-hoc
harshest variant (a tracer counting only ≥75%-filled voxels, median 6.07)
and the 6 mm Cavalieri (6.92) stay far above the registered FAILS bound
of 5.5. **Verdict: FAILS.** No sampling or estimation scheme computable
from what Bhagwandin et al. state turns a ≈7 cm³ hippocampal band into
4.71 cm³. The 4.71-vs-6.97 gap is therefore **not a sampling-estimator
artifact**: it is a between-specimen difference (Direction 1: documented
different animals; Direction 2: shares 0.919% vs 1.548–1.575%) or a
boundary-convention difference inside their unstated operationalization
of "the methodology of Patzke et al. (2015)" — a claim testable only on
their scan, which is not open (Direction 3). Addendum (h)'s candidate (b),
partial-volume thinning, is hereby **retired by computation**.

**What would refute this verdict:** a re-simulation under a scheme
Bhagwandin et al. can be documented to have used (e.g. their true tracing
axis or an area-threshold rule from the Patzke laboratory's protocol)
landing ≤ 5.18 on this mask; or their scan becoming available and
re-tracing at ≈4.71 under T1–T7 (which would move the gap to tracing
convention, on their specimen).

## Direction 5 — Line-side robustness: the anomaly survives, restated at defensible strength

Fit-set transcription verified first: refitting the eight registered
points reproduces the registered line exactly (slope 0.8467, intercept
−1.6609, r 0.930) — the ruler is the ruler.

**(a) Against Patzke's saturating exponential** (`ln Vh = 9.26 × (0.72 −
exp(−0.097 ln Vb))`, as published): at Vb 442.65 the model predicts
4.66 cm³ → the label sits at **+47.0%**, the tight tracing at **+49.5%**
— the registered ≥+30% leg **passes**. The model's own-specimen check is
the striking part: Patzke's compilation value for this species, 7.48 at
Vb 512.55, sits **+49.3%** above Patzke's own model. Two independent
measurement traditions (histology compilation; MRI tracing) place this
species ≈+50% above the saturating mammalian model, while Bhagwandin's
MRI value sits at **−6.0%** against it — on the model. Whatever is
elevated travels with the species/specimen, not with one ruler.

**(b) MRI-class standing** (signed residuals vs the registered line, all
14 points printed with class flags in
`outputs/rhino_anomaly_mri_class_table.csv`): among the 10 direct labels
the rhino's +80.5% ranks **2nd**, behind only the sloth bear's +167.2% —
a label already registered as an artifact (not a bilateral hippocampus
at all). Among **forensically valid** direct labels the rhino is **1st**,
ahead of the ferret's +70.7% (itself explained as form failure,
addendum (i)); the next valid label is the leopard at +10.1%. Share
ranks per Direction 2 (top-2 leg **passes**: 2nd of 5 large-brain direct
labels counting the artifact, 1st of 4 among valid labels).

**(c) Leave-one-out sensitivity (exploratory, declared):** refitting the
line without the rhino (n = 7, slope 0.708, r 0.919) predicts 2.64 cm³ at
442.65 — the rhino's residual *grows* to **+159.6% (label) / +164.0%
(tracing)**. The in-sample caveat on +83.5% therefore cuts against the
anomaly's modesty: the registered line is pulled toward the rhino by the
rhino, and the quoted residual is the conservative version.

**Restatement (registered rule — weakest surviving formulation).** One
leg of the strongest registered formulation ("largest positive
direct-label residual") fails on a technicality that must be printed:
the single larger residual belongs to a label the project has already
registered as an artifact. With that printed, the anomaly is claimed as:

> **The catalogue black rhino's hippocampus is the largest positive
> residual of any forensically valid MRI label (+80.5% label / +83.5%
> tracing against the registered line, in-sample caveat attached), the
> largest hippocampal share of any valid large-brain MRI label (1.548%),
> and ≈+50% above Patzke's saturating model — the same elevation
> Patzke's own histology value shows for this species. It is extreme
> inside its own method class by every ruler available.**

**What would refute the surviving hypothesis:** a same-class MRI
hippocampus census in which this share/residual is unremarkable — in
practice, the Direction 3 second specimen landing ordinary, or a wider
MRI label set reclassifying the share table.

---

## End state

- **Named mechanism:** none. All five registered attacks were run; the
  anomaly survives each: identity (confirmed, and the comparison animal
  separated), profile (insufficient data — the specimen carries no other
  labels), second specimen (none exists openly), estimator (fails by
  computation), ruler (survives Patzke's model, the class ranking, and
  leave-one-out).
- **What the investigation did settle:** the anomaly belongs to this
  specimen (and, at +49% against the saturating model from two method
  classes, plausibly to this species); Bhagwandin et al.'s 4.71 is an
  ordinary measurement of a different, ordinary-shared animal, and is
  retired as evidence *against* the catalogue value; addendum (h)'s
  partial-volume candidate is retired; the record's "no Zenodo rhino"
  premise is corrected (records 44795/44797).
- **The one measurement that would decide between the surviving
  hypotheses** is a second rhinoceros brain MRI, delineated under T1–T7.
  It does not openly exist. Until it does, the rhino residual stands in
  the record as: **doubly measured, five-way attacked, unexplained —
  at the restated strength above.**
