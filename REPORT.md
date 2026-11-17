# Human newborn vs adult lion: a measurement-first comparison of two brains

**Question.** What discrete, measurable anatomical differences exist between a human
newborn brain and an adult African lion brain — from actual scan data, not from
behavioural or evolutionary narrative?

**Design rule.** Nothing here was assumed in advance (not "lions are aggressive", not
"babies lack aggression circuitry"). Every number below is either (a) computed in this
repository from a named scan, (b) taken from a named publication with its n, or
(c) explicitly recorded as **unavailable**. Missing data is never shown as zero.

**The confound, stated once and applied throughout.** This comparison varies species
*and* developmental stage at the same time. No difference below can be attributed to
species alone; §5 quantifies how much of the gap is developmental.

---

## 1. Data actually used

| Side | Dataset | n | What it is | Access |
|---|---|---|---|---|
| Human newborn | **M-CRIB 2.0** (OSF `4vthr`) | 10 term neonates, PMA at scan 40.3–43.0 wk | T1w + T2w + **manual 94-region parcellation** per subject | Open download, no agreement |
| Lion | **Brain Catalogue → Zenodo 44855** (Santin, Herbin & Toro 2016) | 1 adult specimen, age/sex unstated | Post-mortem structural MRI, 0.3 mm isotropic, N4-corrected | Open, CC BY-NC 4.0 |
| Lion (literature) | Sakai et al. 2016, *Front. Neuroanat.* 10:99 | 14 adults (8M/6F) | CT virtual-endocast volumetry | Published |
| Lion (literature) | Jardim-Messeder et al. 2017, *Front. Neuroanat.* 11:118 | 1 | Dissection + isotropic fractionator (mass, neuron counts) | Published |
| Context species | Brain Catalogue (Zenodo), Catlas cat template, MNI152 adult-human template | 12 species + 2 templates | Same ex vivo MRI series as the lion | Open |

What is **not** openly available, after a systematic search (2026-11-16): any lion
segmentation or subcortical volumetry; any lion diffusion MRI; any lion functional
data of any kind; open newborn diffusion/rs-fMRI with segmentations (the dHCP
dataset — 783 neonates — is gated behind NIH NDA collection 3955 with institutional
sign-off; nothing was accessed behind any gate). A labelled domestic-cat atlas
(Catlas, Stolzberg et al. 2017) was downloaded as a *proxy reference only* and is
never presented as lion data.

## 2. The measured delta table

Newborn values are means ± SD across the 10 M-CRIB subjects, computed here from the
manual parcellations (`outputs/human_volumes_per_subject.csv`). Lion specimen volume
was computed here by Otsu-threshold masking (threshold-sensitivity band in
parentheses). Full provenance for every row: `outputs/measurements.csv` (43 rows).

| Measurement | Human newborn (measured, n=10) | Adult lion | Δ / ratio |
|---|---|---|---|
| Total brain volume | **374.4 ± 37.0 cm³** tissue (474.0 incl. labelled CSF) | **188.1 cm³** specimen mask (178–194); species endocranial mean **244.4 cm³** (n=14) | Newborn ≈ **2.0×** the lion specimen; ≈ **1.5×** the lion species mean |
| Cortical gray matter | 160.9 ± 19.0 cm³ — **43.0%** of tissue | Cortex mass 139.9 g — **70.3%** of brain mass (n=1; *mass share, not volume share*) | Not directly commensurable; definitions flagged |
| Cerebral white matter | 161.1 ± 14.1 cm³ — **43.0%** of tissue | **Unavailable** (no validated GM/WM split for lion) | — |
| Cerebellum + brainstem share | 28.8 cm³ — **7.7%** of tissue | 50.5 cm³ — **20.7%** of endocranial volume (n=14) | Lion share ≈ **2.7×** the newborn share |
| Frontal cortex / anterior cerebrum | Frontal (DKT parcels) 52.1 ± 5.7 cm³ — **13.9%** of tissue, 32% of cortex | Anterior cerebrum 17.2 cm³ — **7.1%** of endocranial (n=14) | Newborn share ≈ **2.0×** — *but the two regions are defined by different boundaries; closest available pairing, not homologues* |
| Amygdala | **1.64 ± 0.17 cm³** (0.44% of tissue) | **Unavailable** — no published value; not segmentable with validated tools on n=1 ex vivo scan | — |
| Hippocampus | **2.90 ± 0.31 cm³** | **Unavailable** (same reason) | — |
| Hypothalamus | Not a standalone label; its container (ventral diencephalon) = **2.41 ± 0.22 cm³** | **Unavailable** | — |
| Periaqueductal gray | Not labelled in any open neonatal atlas | **Unavailable** | — |
| Diffusion metrics (FA/MD) | Gated (dHCP/NDA) — not openly computable | No lion dMRI exists openly | — |
| Functional connectivity | Gated (dHCP/NDA) | Post-mortem specimen — cannot exist for this scan; no public in-vivo lion fMRI | — |

Cross-check: an independent published newborn cohort (Wu et al. 2025, *JAMA
Pediatrics*, n=96) gives total brain volume 407.1 cm³, cortical 176.4, white matter
166.7, cerebellum 25.0, brainstem 7.2 — consistent with the M-CRIB measurements
above, except amygdala (1.06 vs 1.64 cm³), a segmentation-protocol difference that
is reported rather than averaged away.

## 3. Visualizations

- **Figure 1** (`outputs/fig1_matched_sections.png`) — matched sagittal/coronal/axial
  sections at each brain's centre of mass: newborn T2 with the 94-region
  parcellation overlaid; lion MRI with the volumetry mask contoured. Scale bars on
  every panel. Matched by plane only; no cross-species voxel correspondence implied.
- **Figure 2** (`outputs/fig2_delta.png`) — absolute volumes and normalised
  proportions, with each bar's denominator printed on the chart.
- **Figure 3** (`outputs/fig3_morphospace.png`) — the morphometric space of §5.

## 4. Interpretation — the largest differences

1. **Size.** A term human newborn's brain tissue (≈374 cm³) is already about twice
   the volume of the scanned adult lion specimen (188 cm³) and ~1.5× the lion
   species' mean endocranial volume (244 cm³, which itself overstates tissue volume
   because endocasts include meninges and CSF space; the lion specimen is also a
   long-fixed ex vivo brain, so some shrinkage is expected). This is a measurement,
   not a ranking: it mostly reflects that the human brain's growth trajectory is
   front-loaded into the perinatal period.
2. **Hindbrain share.** The cerebellum + brainstem occupy ~20.7% of the lion's
   endocranial volume vs ~7.7% of newborn tissue volume — the largest *proportional*
   difference that survives normalisation. (Denominators differ — endocast vs
   tissue — so read the ratio as approximate, ~2.5–2.7×.)
3. **Cortical composition.** At term, the newborn cerebrum is split almost evenly
   between cortical gray matter (43.0%) and white matter (43.0%) — and that white
   matter is largely unmyelinated and water-rich, nothing like adult white matter.
   The lion's cortex is ~70% of brain *mass*. Any "more cortex" claim across these
   two brains is definition-bound; we report the numbers side by side and do not
   merge them.
4. **Frontal share.** The newborn's DKT frontal parcels are 13.9% of tissue vs the
   lion's anterior cerebrum at 7.1% of endocranial volume. The direction is
   consistent with the well-known human frontal expansion, but Sakai's
   anterior-cerebrum boundary is a coronal plane, not a frontal-lobe parcellation —
   so this is the closest available pairing, labelled as such, not a homology.

## 5. The Chen-style layer: a structural morphometric space

Catherine Chen's work embeds brains in a *representational geometry* built from
fMRI responses to shared stimuli. That exact analysis is impossible here — the lion
side has no functional recordings and never will from a post-mortem specimen. What
transfers is the *geometry move*: embed every brain in one shared feature space,
computed identically for all, and read the distances.

Features (from each brain's whole-brain mask): log₁₀ volume; a gyrification proxy
(surface area relative to a sphere of equal volume, all masks resampled to a common
0.6 mm grid first); two elongation ratios from the mask's spatial-covariance
eigenvalues. Points: 10 newborns (individuals), the lion, 11 further Brain
Catalogue species, a domestic-cat template, and the adult-human MNI152 template.
Every mask was visually QC'd (`outputs/qc_contact_sheet.png`); two species were
**excluded** (orangutan — an in-vivo-style scan with skull, not comparable; red
squirrel — header voxel size is a 1.0 mm placeholder, absolute scale lost), the
gray wolf's mask needed morphological closing to seal its cortical shell, and the
dolphin's as-scanned volume sits below species-typical values (flagged; shape
ratios are scale-invariant). Full feature table: `outputs/morphospace_features.csv`.

Distances (Euclidean, in standardised feature space) from the newborn centroid:

| Point | Distance |
|---|---|
| Gorilla specimen | **0.80** |
| Cheetah | 2.42 |
| Adult human (MNI152 template) | 2.86 |
| **Lion** | **2.93** |
| Leopard | 3.01 |
| Gray wolf | 3.67 |
| Domestic cat template / bottlenose dolphin | 4.19 |

The lion's own nearest neighbours are the baboon (1.12), leopard (1.65), gray wolf
(1.69) and giraffe (1.80); lion ↔ adult human = 4.33.

**Reading.** In whole-brain shape geometry, the newborn human brain sits closest to
the gorilla specimen (similar size, similarly compact proportions) — and it is
*about as far from the adult human template (2.86) as it is from the lion (2.93)*.
At the resolution of whole-brain shape, development moves a brain roughly as much
as the species gap in this comparison. The lion, meanwhile, is unremarkable in
shape space: it sits inside a generic large-mammal cluster, not in a felid corner
(its felid neighbour, the leopard, is only its second-closest point). These are
descriptive statements about four shape features at n=1 per species — no
classifier was trained, and none of this licenses functional interpretation.

## 6. What the data can and cannot establish about aggression-related circuitry

- On the newborn side, the relevant structures are measured: amygdala 1.64 ± 0.17
  cm³, hippocampus 2.90 ± 0.31, ventral diencephalon (incl. hypothalamus) 2.41 ±
  0.22. The circuitry is present and quantifiable at term.
- On the lion side, **no homologous regional volume exists in any open dataset or
  publication** — amygdala, hypothalamus, hippocampus and PAG are all unavailable,
  and producing them by hand-drawing on a single ex vivo scan with no validated
  felid protocol would be fabrication, so it was not done.
- Therefore no structural comparison of "aggression circuitry" between these two
  brains can currently be computed. And even with both sides segmented, volume
  alone would not establish activation, predatory motivation, or behavioural
  inhibition — no functional data exist for the lion, and structural MRI intensity
  is not activity.
- What *would* close the gap: a felid subcortical atlas validated on lion MRI (the
  Tennessee felid clinical series holds 11 lion scans but is not public), or a
  published lion histological volumetry series. Neither is openly obtainable today.

## 7. Limitations

Lion n=1 for everything computed here (species literature n=14 for coarse regions
only); the lion specimen is ex vivo and long-fixed (shrinkage, altered contrast);
newborn masks come from manual parcellations while lion/species masks come from
intensity thresholding — method heterogeneity is unavoidable across these sources
and is flagged per row in `measurements.csv`; the morphospace uses four coarse
shape features and template points (MNI152, cat) whose surfaces are smoother than
any individual's, which depresses their folding proxy; the comparison is confounded
by developmental stage by design, and §5 is the control for that, not a cure.

## 8. Reproduce

```
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/volumetry_human.py      # -> outputs/human_volumes_per_subject.csv
.venv/bin/python scripts/volumetry_lion.py       # -> outputs/lion_volume_sensitivity.csv
.venv/bin/python scripts/make_measurements.py    # -> outputs/measurements.csv
.venv/bin/python scripts/figures.py              # -> fig1, fig2
.venv/bin/python scripts/morphospace.py          # -> morphospace CSVs (+ fig3 data)
.venv/bin/python scripts/fig3.py                 # -> fig3
```
Data are **not** redistributed in this repo (licences: M-CRIB — see OSF node
`4vthr`; Brain Catalogue — CC BY-NC 4.0). Download sources and checksums are in
`data/*/PROVENANCE.md`.

## Addendum — 2026-11-16 (later the same day): the catalogue's own segmentations, and a correction

After the report above was finalized, a further check of the Brain Catalogue **website**
(braincatalogue.org — distinct from its Zenodo archive records) found that the project hosts
per-species segmentation files that the Zenodo records omit. This corrects two statements
above: the lion hippocampus is **not** "unavailable" (§2, §6), and §6's list of unmeasurable
lion structures shrinks to amygdala and hypothalamus. The behavioural conclusion of §6 is
unchanged: a hippocampal volume, like every volume here, licenses no inference about
aggression or motivation.

**New measurements on the same lion specimen (catalogue segmentations, overlay-verified):**
hippocampus **2.02 cm³ (1.07% of the 188.1 cm³ brain)**; telencephalon **145.60 cm³ (77.4%)**,
leaving a same-specimen non-telencephalic remainder of 42.5 cm³ (22.6%) — consistent with
Sakai et al.'s hindbrain share (20.7% of endocranial volume, n=14).

**Audit of the full 37-species label set (the verification pass):** the site's files are
uneven. Roughly half the `Hippocampus.nii.gz` files are empty placeholders (correct grid,
zero voxels — e.g. baboon, gorilla, chimpanzee, both macaques, wolf, the catalogue's human).
The red squirrel's "Hippocampus" file duplicates its whole-brain mask. `Atlas.nii.gz` is a
single-label brain mask, not a multi-region parcellation. A few labels are partial
(dolphin and chimpanzee "cerebellum" files are far too small to be the whole structure) and
some carry voxel-size metadata inconsistent with their MRI. Two bulk downloads (lion, zebra
MRIs) arrived as empty files; both species were already held from Zenodo.

**Verified cross-species hippocampus set** (each volume from its own file's voxel size;
denominator = the catalogue's Atlas mask where present, else the Otsu mask, tagged in
`outputs/cross_species_volumes_v2.csv`): ferret 0.17 cm³ (2.8%), cat 0.54 (0.9%*), cheetah
0.85 (1.3%*), red kangaroo 0.20 (0.7%*), giant panda 1.07 (0.6%*), leopard 1.18 (1.2%),
lion 2.02 (1.1%), sloth bear 4.00 (2.1–2.7%), giraffe 2.92 (0.5%*), black rhinoceros 6.85
(1.6%). (* = Otsu-mask denominator, provisional.) A descriptive log–log fit over these ten
species gives hippocampal scaling slope **0.81** (r = 0.90) against brain volume — negative
allometry: bigger brains carry proportionally smaller hippocampi. The M-CRIB newborn
(374.4 cm³ brain, 2.90 cm³ hippocampus) sits **11% below** that mammalian line — close to
it, i.e. at birth the human hippocampus is about the size the generic mammalian scaling
predicts, marginally under. All values n=1 per species, descriptive only.

## Addendum — 2026-11-17: audit corrections, the registered tests, and the residuals resolved

This addendum is appended, not merged: the report body above and the 2026-11-16
addendum stand as written, including the claims this addendum retracts. The record
shows its own history. All tests referenced below were pre-registered in
`PREDICTION.md` (registration commit `d54361f`) before the relevant literature
values were examined, and were executed under its rules — no refitting after the
test sets were seen, missing values reported as missing, method classes never
pooled undeclared. Nothing in this project has been publicly released.

### (a) Retractions — the Reep et al. (2007) audit

A legitimacy audit on 2026-11-17 found the prior art this project had missed:
**Reep, Finlay & Darlington (2007), "The Limbic System in Mammalian Brain
Evolution," *Brain, Behavior and Evolution* 70:57–70** — histological planimetry
(8–10 sections, one hemisphere measured and doubled, shrinkage-corrected) —
published a lion hippocampus volume of **4,496.16 mm³ ≈ 4.50 cm³** (specimen
62-79) and a leopard value of 3.12 cm³, nearly two decades before this project.
Two claims made in this project's summaries are therefore formally retracted:

1. **"Lion hippocampus: first measurement in the literature" — RETRACTED.** The
   catalogue value measured here (2.02 cm³) is the first **MRI-based** value
   only. The first published value is Reep et al.'s 4.50 cm³ (2007).
2. **The unqualified "newborn > lion hippocampus" headline — RETIRED.** It is
   true only inside this project's MRI pipeline (newborn 2.90 ± 0.31 cm³ vs
   catalogue lion 2.02 cm³). Against Reep et al.'s published value the newborn
   is the smaller of the two (2.90 vs 4.50 cm³). Section (c) below shows why
   the cross-method comparison was never licensed in the first place: the two
   method classes disagree systematically, so a headline that silently mixes
   them is not a measurement.

### (b) Felid reconciliation (PREDICTION.md §4; commit `180752a`)

The ~2.2× gap between the catalogue MRI labels (lion 2.022 cm³, leopard
1.178 cm³) and Reep et al.'s histology (4.496 / 3.121 cm³) was tested under the
decision rules registered in advance (gap-closure measured against the
midpoints lion 3.26, leopard 2.15 cm³). Test A — propagating the full D99
hippocampal formation onto the felid MRIs — **failed as an instrument and is
graded VOID**: Dice against the catalogue labels 0.000 (lion) / 0.001
(leopard), centroid offsets 33.2 / 15.9 mm; the cross-order primate→felid
affine landed in the wrong territory. No rescue was attempted. Test B —
boundary sensitivity of the catalogue labels themselves — carried the verdict:
dilating the labels by one voxel closes **15.5%** (lion) / **19.2%** (leopard)
of the gap, inside §4's **<20% band** for both species; even the extreme
two-voxel bound reaches only 34.4% / 38.4% (the mixed band). **Verdict: the
catalogue labels are exonerated as the main explanation.** Delineation
accounts for at most about a third of the gap, and the majority localizes to
the histology side — Reep et al.'s shrinkage-correction multiplier (≈2.4,
resting on estimated shrinkage of 51.8–65%), sparse-section estimation, and
single-hemisphere doubling. Localizing the error is not proof of which exact
step overshot; it is what the registered test could establish, and it is what
it established.

### (c) The blind benchmark (PREDICTION.md §3; commit `6680146`) — the registered line FAILED, and what the failure found

The registered line of §1 was graded blind against 343 published species
(Reep et al. Table 1, n=26, plus the Patzke et al. 2015 compilation, n=317;
no Brain Catalogue species, lion/leopard excluded to §4). **It failed the
registered success criterion decisively:** median absolute percentage error
**66.0%** (mean signed −53.5%) against **18.2%** for the one gradeable
comparator, the Patzke et al. 2015 model; head-to-head 56–287; only 2.0% of
species land within ±25% of the line's predictions. Two declarations accompany
the scorecard: Patzke's model is in-sample on 337 of the 343 test species (a
large structural advantage, declared in `BENCHMARK.md`), and the verdict
survives it — the line also loses the Reep-only subset (55.5% vs 29.2%) and
the both-blind subset of cetaceans/elephant/hippo/manatee (301.6% vs 184.0%).
The second registered comparator, Karbowski (2007), proved **not gradeable** —
its famous −0.14 exponent concerns volume-specific glucose metabolic rate, and
the paper publishes no hippocampal volume equation; nothing was reconstructed
in its place.

The failure decomposes, post-hoc and labelled as such in `BENCHMARK.md`, into
the project's broadest finding — **the Two Rulers**: histological hippocampus
volumes run **~1.6× the MRI-segmentation values at the same brain size,
literature-wide**. The felid offset of §4 is not a felid quirk; it is a
method-class offset between two measurement traditions, and any comparison
that pools them undeclared inherits it. The second component is functional
form: 247 of the 343 test species have brains under 2 cm³, where hippocampal
share climbs to 8–11% and a single power law cannot follow the bend. The
registered line is accordingly retained only as a description of its own
method class (MRI catalogue labels); the claim that it predicts the published
record is dead, and is recorded as dead here rather than quietly dropped.
A by-product of the benchmark's transcription checks: the identity
Vb = Mb/1.036 caught **three dropped-digit typos in Patzke et al.'s published
Table 1** (*Micropotamogale*, *Hipposideros sperois*, *Notopteris*) — excluded
and reported, not silently corrected.

### (d) Chimpanzee propagated point — CIVM corroboration (commit `37234de`)

The chimpanzee hippocampus propagated from the D99 macaque atlas (1.48 cm³)
had stood flagged **PROVISIONAL** pending an independent cross-check, which was
blocked on the CIVM rhesus atlas arriving without a label key. The key was
found in the Scalable Brain Atlas's own per-template key files for CBCetal15
(`index2acr.json` / `acr2full.json`): **hippocampus = label 79** (0.641 cm³ in
the rhesus template). Both earlier empirical candidates were wrong — labels
143 and 158 are cortex (V4V and FST respectively). Propagating label 79 from
the CIVM b0 to the same chimpanzee scan through the project's standard 1 mm
affine pipeline gives **1.56 cm³** — +5.4% against D99's 1.48, −12% against
the modern stereology value of 1.77. **The PROVISIONAL flag is lifted: the
chimp point is corroborated as an affine-propagation estimate.** The standing
caveats are unchanged and are part of the result: both values are affine
propagations, so their agreement cannot exclude a shared method bias, and the
CIVM set is a foreign pipeline (Calabrese et al. 2015), used as cross-check
material only and never pooled into the project's fits.

### (e) Black rhinoceros residual — explained (PREDICTION.md §5; commit `d86cc90`)

The registered +80.5% residual (catalogue label 6.854 cm³ vs 3.80 cm³
predicted at brain 442.65 cm³) was investigated post-hoc, and is so labelled.
**Verdict: label artifact, of the delineation-definition class — not
corruption.** The file is intact (headers, zooms and affines bit-identical to
the MRI; no kangaroo-style metadata copying), correctly placed on overlays,
and its denominator is exonerated (the catalogue mask sits inside the Otsu
sensitivity band re-measured from the rhino MRI itself). Round-two forensics
did correct one first-pass claim: the label is asymmetric by volume (L/R
ratio 0.55), though even the conservative smaller-side ×2 (4.861 cm³) leaves
+28.0%, and boundary looseness accounts for at most about a third under an
extreme assumption. The decisive evidence is a same-specimen literature pair:
Bhagwandin, Haagensen & Manger (2017, *Frontiers in Neuroanatomy* 11:74)
measured **4.71 cm³** by MRI volumetry on a black rhino whose brain mass
(531 g) matches the Patzke compilation row exactly — almost certainly the
same specimen for which the compilation prints **7.48 cm³**, a 1.59× ratio
that reproduces the Two Rulers offset on a single brain. Scaled to this
project's specimen, the catalogue label sits **+65%** above the tight
MRI-protocol expectation (≈4.16 cm³) but only **+3.7%** above the broad
compilation-definition expectation (≈6.61 cm³): the label is, numerically, a
histology-definition measurement living in an MRI dataset. Definition-matched,
the rhino sits on the line (+4 to +10%). Per §6, no refit was taken — the
rhino remains in the n=8 fit set and the registered line is unchanged.

### (f) The confirmatory test left unrun

One test would convert the rhino explanation from inference to demonstration,
and it has not been run: **re-delineate the catalogue rhino MRI under one
declared tight MRI protocol** (the Patzke/Bhagwandin criteria). The
investigation's prediction, recorded here in advance of any such run, is
**≈4.2 cm³** — on the registered line. Until it is run, the delineation-
definition mechanism stands as inference from the numbers and the label's
morphology, not as a documented fact about the catalogue's procedure.

**State of the registered items after this addendum:** §1 line — stands as
registered, descriptive of the MRI-label class only. §2 newborn check —
resolved (−12.0% against the line, as registered). §3 benchmark — executed;
criterion failed. §4 felids — executed; labels exonerated. §5 residuals —
rhino explained (above); the ferret residual (+70.7%, measured 0.173 vs
predicted 0.101 cm³) remains **registered and unexplained** — its label passed
forensics and no investigation has been run. Per-section detail with commit
hashes is in the closing entry of `logs/processing_log.md`.

## Addendum — 2026-11-17 (evening): the three follow-up builds

Commissioned after the record closed; all protocols pre-registered in
`PREREGISTRATION_followups_2026-11-17.md` (commit `86c3636`) before any
measurement. Full records: `outputs/dolphin_delineation.md`,
`outputs/rhino_confirmatory_redelineation.md`, `outputs/ferret_forensics.md`.
Nothing in the body or prior addenda is altered; where this addendum
supersedes an earlier statement, it says so.

### (g) Item 1 — Dolphin hippocampus delineation: FAILED at QC, no volume claimed

The Brain Catalogue's hippocampus files for both dolphins are empty
placeholders, so a delineation was attempted on the bottlenose MRI
(0.30 mm; Atlas denominator 515.46 cm³) under a registered protocol
(hippocampal-formation definition and landmarks from Montie et al. 2007/
2008; CSF-landmark calibration verified against the catalogue's own lion
and cat labels). The traced object measured 3.44 cm³ — and **failed
registered QC gates (a) and (d)**: sagittal/axial overlays show a
rectangular slab of medial temporal (parahippocampal/perirhinal) cortex
crossing cortical folds, not a lamina in the medial wall of the inferior
horn, and 3.44 cm³ is outside the registered 0.3–2.0 cm³ sanity band.
Re-inspection concluded the anatomy does not genuinely read as a
3.44 cm³ hippocampus: in this extracted, formalin-fixed specimen the
ventral/medial CSF borders that bound the formation in situ are
collapsed, so the formation is not separable from the parahippocampal
cortex in this contrast. Montie et al. 2007 state the same conclusion
for this specimen class in print — the bottlenose dolphin is named among
the species whose hippocampus could not be identified in formalin-fixed
brain MRI, by exactly this mechanism. **No hippocampus volume is claimed
for either dolphin** (La Plata: same verdict on inspection). The
registered expectation (residual −70 to −95%) is neither confirmed nor
refuted; the test failed at the measurement stage and is recorded as
failed, not rescued. What would make the measurement possible: an
in-situ-style T2/PD scan, the catalogue team's own cetacean delineation,
histology of the specimen, or an expert cetacean tracing. The aquatic
thread's conclusion stands unchanged: no MRI-label hippocampus exists
for any aquatic species.

### (h) Item 2 — Rhino confirmatory re-delineation: the §(f) prediction is REFUTED

The test left unrun in §(f) has now been run, under the registered tight
protocol T1–T7. **Fresh delineation of the catalogue rhino MRI =
6.97 cm³** (sides 2.41 / 4.57; the label's asymmetry reproduces), ±1-voxel
sensitivity −28.2% / +21.9% (erode-1 = 5.01 cm³). Verdict against the
fixed bands: **REFUTED** (≥5.48). The declared exclusion classes
(fimbria thread, dust) total only 1.5% of the label; the label's bulk is
the MRI-visible lamina band, and the band measures ~7 cm³ under the
tight criteria — even a uniformly one-voxel-tighter tracing (5.01) stays
above the CONFIRMED ceiling (4.83). **This supersedes §(e)'s and §(f)'s
framing:** the delineation-definition mechanism, as operationalized by
its own registered test, fails; the rhino residual **reopens** at
+83.5% vs the registered line, unexplained by denominator, exclusions,
boundary placement, or definition. The evidence inverts: two MRI
tracings (catalogue 6.854, this one 6.97) agree with each other and sit
1.09× below Patzke's histology value (7.48), while Bhagwandin et al.
2017's MRI value (4.71) becomes the low outlier — candidate explanations
declared and untested (different specimen; 2 mm partial-volume thinning
in Bhagwandin's tracing; genuinely large hippocampus in this specimen).
No refit taken (§6).

### (i) Item 3 — Ferret residual: FORM FAILURE (post-hoc)

The ferret's registered +70.7% residual was forensically investigated
(sequence declared in advance; verdict post-hoc per §5). Label integrity
**clean**: header/affine identical to the MRI; two components hold
99.994%; per-side volumes 0.0872 / 0.0860 cm³ (ratio 0.986 — symmetric
by volume); position verified on overlays in three planes. (Catalogue
note: the ferret Neocortex label overlaps 67.3% of the hippocampus
label — the "Neocortex" file is the full cortical sheet drawn over the
medial wall; a property of that label, not of this one.) Denominator
**exonerated**: Otsu band 5.97–6.27 cm³, residual +67.7% to +74.8%
across it; a zero residual would need an 11.55 cm³ brain, which no
published ferret value approaches. Literature: Patzke's compilation has
no *M. putorius* row; the least weasel stands at +315.9% vs the line;
Hutchinson et al. 2017's ferret MRI templates put the hippocampus at
3.63% of brain volume — *above* this specimen's 2.83%. And the line's
demonstrated median error in the ferret's size band (2–20 cm³) is
69.0%: the ferret's +70.7% is a typical miss of the power-law form in
that range, while Patzke's saturating exponential deviates the other
way (−48.0%). **Verdict: form failure** — the power law's known
small-brain under-prediction, measured on one of its own fit points.

**State of the registered items after this addendum:** §1 line — stands,
unrefitted. §5 residuals — rhino: **reopened** by (h), +83.5%,
unexplained; ferret: explained post-hoc as form failure by (i). Item 1
closes with no measurement: the dolphin hippocampus is not delineable
from the catalogue scans under the registered landmarks, for the reason
the primary literature gives. No registered items remain outstanding;
the rhino residual is the record's one open anomaly.

## Addendum — 2026-11-17 (night): the rhino anomaly investigation — five attacks, anomaly survives

Commissioned by Atharva after addendum (h) reopened the rhino residual;
all five directions pre-registered in
`PREREGISTRATION_rhino_anomaly_2026-11-17.md` (commit `e53edfd`) before
any test was run. Full record: `outputs/rhino_anomaly_investigation.md`;
numbers: `outputs/rhino_anomaly_results.json`. Body and addenda (a)–(i)
untouched; where this addendum corrects an earlier statement, it says so.

### (k1) Specimen identity — CONFIRMED; the comparison animal is separated, and a record premise is corrected

The catalogue rhino MRI is **Zenodo record 44797** (Santin, Herbin &
Toro, 2016-01-15, CC BY-NC 4.0); the local file is md5-identical to the
deposit, and the mesh is record 44795. *This corrects the framing left
by the 2026-11-16/17 addenda:* the rhino was inside the catalogue's
Zenodo deposit family all along — `data/brain_catalogue/PROVENANCE.md`
had enumerated only the morphospace downloads. The documented chain
(deposit → species page → Herbin's Vertebrate Brain Collection, Jardin
des Plantes, scanned at ICM/CENIR Paris) names *Diceros bicornis* at
every link; no sex, age or individual ID exists anywhere in it. The
metadata-swap failure mode does not apply. And the catalogue specimen is
**documented to be a different animal** from the Patzke/Bhagwandin
specimen (40-year-old male, National Zoological Gardens Pretoria, Wits
Philips 1.5 T, 531 g; the catalogue brain's mass-equivalent is 458.6 g) —
the "same specimen" inference in §(e) was always Patzke-row ↔
Bhagwandin, and it stands; the catalogue animal was never that animal.

### (k2) Whole-brain profile — INSUFFICIENT (registered rule)

The specimen carries exactly two catalogue labels (Atlas mask,
Hippocampus). Bhagwandin et al. publish same-species MRI references for
cerebellum, amygdala and ventricles, but no labels for those structures
exist in this specimen, so the registered minimum for a
specimen-vs-structure verdict (two referenced structures) is not met and
no such verdict is claimed. Descriptively: hippocampal share is 1.548%
(label) / 1.575% (tracing) in this specimen against 0.919% in
Bhagwandin's — in share space the anomaly is a between-specimen fact,
n = 1 against n = 1, declared.

### (k3) Second specimen — NONE OPENLY AVAILABLE (checked claim)

The full registered search protocol (catalogue census, Zenodo by web
index and direct API, MorphoSource, OpenNeuro, NITRC, post-2017
literature, general web) finds no other rhinoceros brain MRI openly
downloadable, of any species. Bhagwandin et al.'s black and white rhino
scans were never deposited; post-2017 rhino brain imaging is CT
endocasts (Iurino et al. 2020), a different modality. Declared
limitation: MorphoSource/OpenNeuro were searched via the web index, not
native internal search. The world's open rhino brain MRI supply is this
one specimen.

### (k4) Bhagwandin reconciliation — FAILS; the partial-volume candidate is retired

Bhagwandin et al. state no estimator (their Volumetrics paragraph
delegates hippocampal calculation to "the methodology of Patzke et al.
(2015)"); the verbatim scheme is not computable as stated. Against the
registered declared proxies, simulated on the tight mask across all
phase offsets: 2 mm contiguous slabs (their stated acquisition) give a
phase-median of **7.21 cm³** — partial-volume averaging at 2 mm does not
thin a ≈9.5 mm lamina, it slightly fattens it; Cavalieri at the 6 mm
figure spacing gives 6.92; even a post-hoc ≥75%-fill threshold gives
6.07. Nothing approaches 4.71. **The 4.71-vs-6.97 gap is not a
sampling-estimator artifact.** Addendum (h)'s candidate (b) —
partial-volume thinning in Bhagwandin et al.'s tracing — is retired by
computation. What remains is a between-specimen difference (k1, k2) or a
boundary convention inside their unstated operationalization, testable
only on their scan, which is not open (k3).

### (k5) Line-side robustness — restated strength

Against Patzke et al.'s saturating exponential, the rhino sits at
**+47.0% (label) / +49.5% (tracing)** at 442.65 cm³ — and Patzke's own
compilation value for the species sits at **+49.3%** against Patzke's
own model, while Bhagwandin's 4.71 sits at −6.0%. Inside the MRI class,
the rhino's residual is the largest of any forensically valid direct
label (the one larger value, the sloth bear's, belongs to a label
registered as an artifact), and its 1.548% share is the largest of any
valid large-brain direct label. A leave-one-out sensitivity (declared
exploratory) grows the residual to +160–164%: the in-sample caveat on
+83.5% makes the quoted figure the conservative one. **Restated
anomaly:** doubly measured at 6.854/6.97 cm³; extreme inside its own
method class by every ruler available (registered line, Patzke's model,
within-class ranks); ≈+50% above the saturating mammalian model from
two independent method classes, for this species.

**State of the registered items after this addendum:** the rhino
residual remains the record's one open anomaly — now five-way attacked
(identity, profile, second specimen, estimator, ruler) and unexplained,
with two candidate explanations formally retired (delineation
definition, addendum (h); partial-volume thinning, this addendum) and
the surviving hypotheses ranked in
`outputs/rhino_anomaly_investigation.md`: genuine species/individual
elevation; a rhino-specific non-formation component inside the lamina
band, namable only with histology that does not openly exist; an
individual anomaly of the world's only openly scanned rhinoceros. The
deciding measurement — a second rhino brain MRI under T1–T7 — does not
openly exist.
