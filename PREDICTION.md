# Pre-registered predictions and benchmark protocol

**Registered: 2026-11-17.** The git commit carrying this file is the registration
record. Everything below was fixed *before* extracting or examining any
literature test-set values, with two declared exceptions: the Reep et al. (2007)
lion and leopard hippocampus volumes, which surfaced during the 2026-11-17
leaderboard audit and are therefore handled by the separate, non-blind felid
reconciliation test (§4), never by the blind benchmark (§3).

## 1. The registered line (primary)

Fitted on the Brain Catalogue label set after forensic QC
(`outputs/cross_species_volumes_v3.csv`, `outputs/label_forensics.csv`):

```
log10(hippocampus_cm3) = -1.6609 + 0.8467 × log10(brain_cm3)
n = 8, r = 0.930, p = 8.1e-4
```

Fit set (catalogue labels only): black rhinoceros, cat, cheetah, ferret,
giant panda, leopard, lion, red kangaroo.

Exclusions, with reasons fixed in advance:
- **Sloth bear** — label artifact: both main components on the same side of the
  midline (not a bilateral hippocampus).
- **Giraffe** — label unilateral: second component is 1.3% of the first.

Declared sensitivity fit (not primary): the unfiltered n=10 headline line,
slope 0.8089, intercept −1.5665, r 0.897. The red kangaroo label's header
metadata is corrupt (copied from the sloth bear files); refitting it at its own
MRI's zooms moves the QC slope to ≈0.82 — noted here so the variant cannot be
cherry-picked later.

Model-estimated (atlas-propagated) points — catalogue human, chimpanzee,
gorilla, gray wolf — never enter any fit set.

## 2. Registered point check (already measured, not blind)

- **Newborn human (M-CRIB 2.0, n=10):** the line predicts 3.30 cm³ at a brain
  volume of 374.4 cm³; measured 2.90 ± 0.31 cm³ → **−12.0%**. Registered as a
  confirmation target: the newborn sits modestly below the adult cross-species
  line, stable across every fit variant tried (−11% to −15%).

## 3. The blind benchmark

**Test set:** every species with a published hippocampus volume in Stephan et
al.'s dissection series, Reep, Finlay & Darlington (2007, Table 1), or the
Patzke/Manger compilation that is (a) not among the Brain Catalogue's 37
specimens and (b) not the lion or leopard (already seen; §4).

**Procedure:** for each test species, take the literature brain volume and
hippocampus volume as published. Predict hippocampus volume from brain volume
using the registered line (§1). Apply the published comparator equations —
Karbowski (2007) hippocampal scaling and the Patzke et al. regressions — to the
same species, identically.

**Metrics (primary first):**
1. Median absolute percentage error across the test set.
2. Mean signed percentage error (bias).
3. Head-to-head win/loss count against each comparator.

**Success criterion, declared in advance:** the registered line counts as
"predicting unseen anatomy better than existing models" only if its median
absolute percentage error is lower than *each* comparator's on the same species
set. The scorecard is published in the project report regardless of outcome.

## 4. Felid reconciliation test (non-blind; values already known)

Reference values — catalogue MRI labels: lion 2.022 cm³ (1.07% of brain),
leopard 1.178 cm³ (1.19%). Reep et al. (2007) histological planimetry:
lion 4.496 cm³, leopard 3.121 cm³.

**Test:** re-delineate both hippocampi on the catalogue MRIs under the
Reep/Stephan boundary rules (hippocampal formation including dentate gyrus,
cornu ammonis and subiculum), and measure.

**Decision rules, fixed in advance** (gap-closure measured against the
midpoints lion 3.26 cm³, leopard 2.15 cm³):
- Re-delineated volumes close **≥50%** of the gap → delineation/definition is
  the main driver; the catalogue labels are the conservative side.
- Closure **<20%** → catalogue labels exonerated; the discrepancy points at the
  histological side (shrinkage-correction multiplier, sparse-section
  estimation, single-hemisphere doubling).
- **20–50%** → mixed; report the decomposition, claim neither side.

## 5. Registered residuals (unexplained; no story attached)

Against the registered line, with forensically clean labels:
- **Black rhinoceros +80.5%** (measured 6.854 vs predicted 3.80 cm³)
- **Ferret +70.7%** (measured 0.173 vs predicted 0.101 cm³)

Any explanation offered later for these two must be labelled post-hoc.

## 6. Rules

- No refitting after the test set is seen. Any revised line is a new dated
  registration in a new commit.
- Missing literature values are reported as missing, never imputed.
- Method classes (direct label / literature dissection / model estimate) are
  never pooled undeclared.
