# Black rhinoceros hippocampus residual — investigation

**Run:** 2026-11-17 · **Scripts:** `scripts/rhino_investigation.py`,
`scripts/rhino_label_shape.py`, `scripts/rhino_final_numbers.py`
**Status: POST-HOC in full.** The residual was registered unexplained in
`PREDICTION.md` §5 (measured 6.854 cm³ vs 3.80 cm³ predicted by the registered
line at brain 442.65 cm³, **+80.5%**). Everything below is an explanation
offered after the fact and is labelled as such. No refitting was done or is
licensed by this report (`PREDICTION.md` §6). No public release.

## Verdict

**LABEL ARTIFACT — of the delineation-definition class, not corruption.**
The file is intact, correctly registered, and in the right anatomy; but the
catalogue's rhino label was drawn under a materially broader delineation than
the MRI-protocol measurements the registered line describes. Compared
like-for-like against the published MRI-protocol value for this species, the
label reads **+65%** high; compared against the broader histology-compilation
definition, it reads **+3.7%** — it is, numerically, a histology-definition
measurement living in an MRI dataset. The denominator is exonerated. After
definition-matching, the rhino sits on the line (+4 to +10%), inside ordinary
scatter. The registered +80.5% residual is explained post-hoc.

## Test 1 — Label forensics, round 2

**Header/affine integrity: CLEAN (no kangaroo-style corruption).** MRI, Atlas
mask and Hippocampus label share shape (265×328×143), zooms (0.45 mm iso) and
bit-identical affines; axcodes LAS. The label reproduces 6.854 cm³ at its own
zooms and at the MRI's zooms (they are the same).

**Components (26-conn):** 61 components; the top two hold 98.9% (R 4.352 cm³,
L 2.428 cm³). The remaining 59 are dust totalling 0.074 cm³ (1.08%), scattered
up to 31 mm from the main components — noise, not anatomy. Accounting:
bulk slab (ax1 140–214) 6.781 cm³; a thin anterior thread (ax1 <140) of
0.031 cm³ — the fimbria/fornix course, which the Stephan/Reep definition
explicitly includes — and 0.042 cm³ of posterior dust. Top-2 components only:
6.780 cm³ (residual would still be +78.5%).

**Position: verified on overlays** (`outputs/segmentations/qc_rhino_*.png`).
The label forms the hippocampal arch in the medial temporal lobe bilaterally —
axial slices show it wrapping the temporal horn; sagittal slices trace the
dorsal-to-ventral curve. No spill into ventricle lumen or distant cortex.
Median S-I column thickness 9.5 mm (a curved lamina, not a solid slab).

**Asymmetry (new in round 2):** the sides are unequal — L 2.431 vs R 4.424 cm³
(ratio 0.55), in the bulk as well as the whole label. The first pass called the
label "symmetric" from centroid positions; by volume it is not. Even the
conservative symmetrization (smaller side ×2 = 4.861 cm³) leaves a +28.0%
residual, so asymmetry alone does not explain the residual either.

**Boundary sensitivity** (`outputs/rhino_boundary_sensitivity.csv`), felid
Test-B style, lion label as control:

| | base | erode 1 vox | dilate +1 vox | dilate +2 vox |
|---|---|---|---|
| Rhino (0.45 mm vox) | 6.854 | 4.417 (−35.6%) | 9.725 (+41.9%) | 12.718 (+85.5%) |
| Lion (0.30 mm vox) | 2.022 | 1.390 (−31.3%) | 2.404 (+18.9%) | 2.873 (+42.1%) |

Per millimetre of shell the rhino's sensitivity is comparable to the accepted
lion label's — the signature of a thin, curved structure, not of a fat pen.
The extreme bound (a pen a full voxel too generous on every surface, i.e. the
eroded volume 4.417 cm³) would still leave +16.3%. Boundary looseness can
contribute; it cannot carry the residual alone.

## Test 2 — Denominator check: EXONERATED

The fit used the catalogue Atlas mask, 442.65 cm³. Re-measured from the rhino
MRI itself (Otsu, lion method, largest component + hole filling):

| threshold | brain volume |
|---|---|
| Otsu ×0.8 | 474.0 cm³ |
| Otsu ×0.9 | 448.9 cm³ |
| Otsu ×1.0 | 426.8 cm³ |
| Otsu ×1.1 | 391.1 cm³ |
| Atlas mask | 442.65 cm³ (Dice vs Otsu@1.0: 0.930) |

The mask sits inside the Otsu sensitivity band — it is not an undercount.
Residuals under each denominator: +80.5% (mask), +86.2% (Otsu ×1.0), +78.4%
(×0.9), +100.4% (×1.1). Even substituting the largest published brain volume
for the species (512.55 cm³, a different and larger specimen) leaves +59.4%.
**The residual is not a denominator error.**

## Test 3 — Literature check

- **Patzke et al. 2015, Table 1** (transcribed in `scripts/benchmark.py`;
  row checksum Vb = Mb/1.036 passes exactly): *Diceros bicornis* —
  Mb 531.00 g, Vb 512.55 cm³, **Vh 7.48 cm³**, source code 5 (the authors' own
  study). This row was excluded from the §3 benchmark only because the
  catalogue specimen is the same species.
- **Reep et al. 2007, Table 1:** no rhinoceros of any genus (verified against
  the full transcription).
- **Bhagwandin, Haagensen & Manger 2017** (*Front. Neuroanat.* 11:74;
  PMC5583206, opened and read): MRI volumetry of a 40-year-old male black
  rhino — brain mass **531 g, identical to the Patzke row's Mb**, i.e. almost
  certainly the same specimen — using Patzke et al. (2015) anatomical criteria
  on the MR images: **hippocampus 4.71 cm³**. White rhino (536.5 g):
  3.97 cm³. The authors note both fall within the 95% prediction intervals of
  the mammalian regression.

So the Manger lab has published two values for (almost certainly) one brain:
**7.48** (compilation table) and **4.71** (MRI delineation) — a ratio of
**1.59×**, reproducing on a single specimen the ~1.6× histology-vs-MRI method
offset the §3 benchmark found literature-wide.

Against the registered line: Bhagwandin's MRI value sits at +9.6%
(4.71 vs 4.30 predicted at 512.55) and the white rhino at −8.3% — **on the
line**. Scaled to our specimen's brain (442.65, factor 0.883 at the line's
slope): the tight MRI-protocol expectation is ≈4.16 cm³ (our label: **+65%**
above it); the broad compilation-definition expectation is ≈6.61 cm³ (our
label: **+3.7%** above it). The catalogue label matches the second, not the
first. Even after correcting the compilation value by the full method offset
(line ×1.58 = 6.00 expected vs 7.48 actual), the species' broad-definition
measurement remains +24.7% high — the definition gap is the dominant term,
not noise.

## Test 4 — Comparative sanity (numbers only)

Hippocampus as % of brain. Within our MRI/catalogue data the rhino label
(1.548%) is the highest share among large brains — giraffe bilateral-equivalent
0.943%, lion 1.075%, leopard 1.188%, cheetah 1.248%, panda 0.586% — i.e. it
stands alone in its own method class. In the histology record, large
herbivores do sit high (zebu 1.548%, camel 1.550–1.716%, zebra 2.398%, llama
2.169%), but histology shares run ~1.6× MRI shares across the board (lion:
1.946% histology vs 1.075% MRI). The one like-for-like comparison — the
published MRI-protocol rhino, share 0.919% — is unremarkable next to the other
MRI shares. **The rhino is not part of a large-herbivore elevation once method
classes are kept separate; the apparent pattern is the method offset wearing
a clade costume.**

## Decomposition and what would settle it

Of the registered +80.5%: denominator ≈ 0 points (Test 2); dust/thread ≈ 1
point (top-2-only residual +78.5%); boundary looseness at most ~⅓ under an
extreme assumption (erosion bound +16.3%, not supported as a defect by the
lion control); the balance is the delineation definition — the label
quantitatively belongs to the broad (compilation/histology) definition class
in an MRI fit set. Confirmatory test, not run here: re-delineate the
catalogue rhino MRI under one declared tight MRI protocol (the
Patzke/Bhagwandin criteria) — the prediction of this report is ≈4.2 cm³,
i.e. on the line. The catalogue's written delineation protocol for this
specimen was not available; the definition-class mechanism is inferred from
the numbers and the label's morphology, and is stated as inference, not as
a documented fact about the catalogue's procedure.

**Consequence for the registered line:** none taken. The rhino was a member
of the n=8 fit set; `PREDICTION.md` §6 forbids refitting after the fact
outside a new dated registration. This report explains the residual; it does
not move the line.
