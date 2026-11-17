# CIVM rhesus label-key hunt — outcome: **FOUND AND VERIFIED**

**Date:** 2026-11-17 · **Scope:** identification only (no propagation run)

## Answer

In `civm_rhesus_v1_labels.nii.gz` (Scalable Brain Atlas template **CBCetal15** =
Calabrese et al. 2015, Duke CIVM postmortem rhesus DTI atlas):

| Structure | Label value | Volume in our file |
|---|---|---|
| **Hippocampus ("Hip")** | **79** | **0.641 cm³** (189,780 vox) |
| Amygdala | no single value — 19 subnuclei, labels **56–78** | ≈ **0.49 cm³** summed |

**Neither prior candidate was the hippocampus:**
- **143 = V4V** (ventral V4, visual cortex) — 0.634 cm³. Its ventral sweep along the
  occipitotemporal surface mimicked a hippocampal-formation position on slices.
- **158 = FST** (fundus of the superior temporal sulcus area, cortex) — 0.381 cm³.
  A cortical sheet, not a subcortical structure.

## The key source

The Scalable Brain Atlas serves per-template key files that the original crawl
never inventoried (it captured the `source/` files only). From the template's own
directory, fetched live 2026-11-17:

- `https://scalablebrainatlas.incf.org/templates/CBCetal15/template/index2acr.json`
  — voxel value → acronym (278 entries, indices 1–278; **79 → "Hip"**)
- `https://scalablebrainatlas.incf.org/templates/CBCetal15/template/acr2full.json`
  — acronym → full name (**"Hip" → "hippocampus"**)
- (`index2rgb.json` and `rgb2acr.json` also exist there; `index2full.json` 404s.)

Copies saved beside this report: `outputs/civm_rhesus_v1_index2acr.json`,
`outputs/civm_rhesus_v1_acr2full.json`.

Key structure note: indices 1–241 are the atlas's leaf structures (the voxel
values); indices 242–278 in `index2acr.json` are SBA hierarchy/parent nodes
(e.g. 264 "hippocampus" as a grouping, 269 "subpallial amygdala") and are
**absent from the voxel file, as expected**. Only 79 is the hippocampus label.

## Verification against our file (all checks pass)

- **Coverage is exactly 1:1.** The file holds 241 nonzero labels, values 1–241,
  total labelled volume 74.32 cm³ (22.0M vox @ 0.15 mm) — matching the paper's
  "segmentation of 241 anatomic structures" and the hunter's verified totals.
  Every file value has a key entry; every key leaf (1–241) is present.
- **Hippocampus (79):** 0.641 cm³ — inside the expected 0.3–0.9 cm³ band.
  Exactly **2 components of exactly equal size (94,890 vox each)**, top-2 share
  1.000 — the mirrored pair the symmetrized template guarantees. Ventral
  medial-temporal position, elongated curved extent (bbox 208×106×119 vox).
- **Amygdala control:** the 19 subnuclei (AHi, AA, BSTIA, CeL, Cem, AHiMC, AHiPC,
  APir, BL, BLD, BLI, BLV, BLVL, BLVM, BM, La, Me, PaL, VCo; labels 56–78) are
  each small (0.006–0.071 cm³), each an exactly-equal mirrored pair, all clustered
  **anterior and ventral to the hippocampus**, summing to ≈0.49 cm³ — the expected
  total amygdala range (~0.3–0.6 cm³).
- **Landmark controls:** 1 = LV (ventricles, 0.359 cm³, central), 2 = Md (medulla,
  posterior-inferior, single component), 4 = Cb (cerebellum, 7.09 cm³, most
  posterior), 5 = MB (midbrain, 1.34 cm³), 240 = cwm (cerebral white matter,
  largest at 18.9 cm³), 110 = V1 (3.51), 111 = V2 (3.0), 55 = Pu (putamen, 1.6),
  53 = Cd (caudate, 1.23). Every landmark sits where the key says it should.
- The candidates' true identities are anatomically consistent with why they
  fooled the position screen: both are ventral temporal **cortical** sheets with
  near-whole-hemisphere rostrocaudal extents (143 bbox spans 336 vox along the
  long axis; 158 spans 328) — unlike the compact hippocampal arc.

## Routes tried

1. **Gold directory itself** — only the 3 NIfTI files (labels, b0, Badhwar atlas);
   no readme/labels file was overlooked. NIfTI headers of the labels and b0 files
   carry **no** embedded key: `descrip`, `aux_file`, `intent_name` all empty, no
   header extensions. The hunter's `outputs/sba-inventory.json` did identify the
   SBA template code (**CBCetal15**) and the `templates/CBCetal15/source/` URLs —
   the thread that led to the key.
2. **Duke CIVM (origin)** — `civm.duhs.duke.edu/rhesusatlas` survives but now
   gates downloads behind CIVMVoxPort registration; no open label list there.
   The paper (Calabrese et al. 2015, *NeuroImage* 117:408–416, PMC4512905) names
   its label list as **Supplementary Table 2** (`NIHMS696288-supplement-4.xlsx`,
   24.3 KB, linked from PMC). Located but **not retrievable**: PMC's bin download
   returns a "Preparing to download" interstitial to both curl and the page
   fetcher, the Europe PMC mirror returns 403, and the NCBI OA utility endpoint
   404s. Not needed — route 3 is the distribution's own key — but recorded as the
   one loose end if a second, paper-side confirmation is ever wanted.
3. **Scalable Brain Atlas alternate routes** — **SUCCESS** (above). The previously
   404'd `macaque/wholebrain_labels.csv` belongs to the SBA *wholebrain surface*
   template (a different numbering system, PHT00-lineage); it was correctly never
   applied to this file.
4. **NITRC / mirrors** — web searches surfaced no NITRC (or other) mirror of the
   CIVM rhesus atlas distribution; the atlas circulates via Duke VoxPort and SBA.
5. **Wayback Machine** — not required: the live SBA template files resolved the
   key. (The hunter's archived SBA captures covered other templates' cache
   images, not CBCetal15 keys.)

## For the cross-check that consumes this

- CIVM rhesus hippocampus (label 79, this file): **0.641 cm³** at a total
  labelled brain volume of 74.32 cm³ — same-pipeline CIVM numbers, to be used
  as cross-check material only, never pooled undeclared (standing rule).
- Method note for whoever runs it: the file is the **symmetrized** template —
  every bilateral label is two exactly-equal components; per-side volume is
  exactly half the total.
