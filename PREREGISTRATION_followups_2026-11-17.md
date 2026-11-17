# Pre-registration — 2026-11-17 follow-up builds (Items 1 and 2) and declared analysis plan (Item 3)

**Registered: 2026-11-17, after the fold-in commit `5576c55`.** The git commit
carrying this file is the registration record. It governs two builds
commissioned by Atharva on 2026-11-17, in his priority order. Project rules
carry over unchanged (`PREDICTION.md` §6): no refitting of the registered
line; missing = missing, never zero; method classes never pooled undeclared;
failed or void tests recorded as failed/void, never rescued silently. Nothing
public.

The registered line used throughout as a fixed ruler (never refitted):

```
log10(hippocampus_cm3) = -1.6609 + 0.8467 × log10(brain_cm3)   (n = 8, r = 0.930)
```

---

## Item 1 — Dolphin hippocampus delineation (Brain Catalogue specimens)

### Why

Both dolphin Hippocampus files in the Brain Catalogue are empty placeholders
(nz = 0; `aquatic/REPORT_aquatic.md` §2), so no MRI-class cetacean point
exists in the catalogue class the registered line is fit on. The bottlenose
MRI on disk shows the hippocampal formation. This build delineates it under
the protocol below.

### Prior art, declared before measuring (novelty scope)

- **Montie et al. 2008** (*Anat. Rec.* 291:263–282) measured hippocampus
  volume from in-situ MRI in the Atlantic white-sided dolphin
  (*Lagenorhynchus acutus*) — the first MRI volumetry of any cetacean
  hippocampus. Patzke et al. 2015 Table 1 carries their value as 1.73 cm³ at
  Vb 1,267.57 (mean of 3 specimens). **This build is therefore NOT the first
  MRI-class cetacean hippocampus measurement.** Its scope: the first
  delineation on a Brain Catalogue cetacean scan (the method class of the
  registered line's fit set), and the first MRI-class values for
  *Tursiops truncatus* and *Pontoporia blainvillei* if they land.
- Patzke et al. 2015 (Table 1, histology class unless noted): bottlenose
  1.05 cm³ at Vb 1,476.83; the four literature cetaceans sit at residuals
  −81.3% to −92.0% against the registered line (aquatic §3b; the −81.3%
  point is Montie's MRI value, the rest histology).

### Specimens

- **Primary:** Bottlenose dolphin, `data/brain_catalogue_full/Bottlenose_dolphin/MRI-n4.nii.gz`
  (447×380×224, 0.301×0.301×0.300 mm). Denominator: catalogue Atlas mask,
  **515.46 cm³** (aquatic §2; the specimen is well below the species-typical
  ~1,477 cm³ — flagged there and here).
- **Secondary (attempt):** La Plata dolphin, `.../La_Plata_dolphin/MRI.nii.gz`
  (316×321×160, 0.25 mm iso). No whole-brain denominator exists (aquatic §2:
  Otsu output = the telencephalon label, 91.29 cm³). Placement, if the
  delineation lands, uses only a literature brain volume verified during the
  build (candidate source: Schwerdtfeger, Oelschläger & Stephan 1984,
  *Anat. Embryol.*, the quantitative neuroanatomy of this species, cited by
  Patzke et al. 2015); if none verifies, the volume is reported unplaced.

### Structure definition (fixed)

Hippocampal formation = **dentate gyrus + cornu ammonis + subiculum**,
including the alveus on the ventricular surface; **excluding** entorhinal and
parahippocampal cortex, **excluding** the amygdaloid complex, **excluding**
fimbria/fornix beyond the alveus. This is the Reep/Stephan boundary family
registered for the felids in `PREDICTION.md` §4, so the new points are
definition-consistent with the fit set's class. Sources: Reep et al. 2007
(formation incl. DG, CA, alveus, fimbria caudal to septum — the fimbria
exclusion here is the one declared deviation, matching what an MRI tracing
can separate); Patzke et al. 2015 (all formation components present in
cetaceans, markedly reduced; DG loosely organized); Hof et al. 2005 via
Patzke et al. 2015 (in *Tursiops* the DG is unfolded and the hippocampal
fissure open — the fissure is therefore a usable surface landmark, not a
fused seam).

### Position and boundary landmarks (fixed)

- The formation lies in the **medial wall of the inferior (temporal) horn of
  the lateral ventricle**, ventromedial temporal lobe.
- **Rostral limit:** the temporal pole of the hippocampus, caudal to the
  amygdaloid complex, separated from it by the incursion of the lateral
  ventricle (the topography stated for the rhino in Bhagwandin et al. 2017;
  standard mammalian topography, and the boundary Montie et al. traced
  against).
- **Caudal limit:** the last coronal slice on which the formation remains a
  coherent lamina in the medial wall of the inferior horn, before the tail
  thins toward the trigone.
- **Medial limit:** the hippocampal fissure / pial surface. **Lateral
  limit:** the ventricular surface (alveus against the inferior horn's CSF).

### Procedure (fixed)

1. Work in the coronal plane (axis 1), hemispheres separately (split at the
   Atlas mask's centroid plane on axis 0).
2. Segment CSF candidates inside the Atlas mask by intensity (in-mask low
   tail, threshold declared in the run script) and identify the inferior
   horn component in each temporal lobe by continuity across slices.
3. Calibrate gray/white intensity bands per scan from declared sample boxes
   (cortical ribbon remote from the temporal lobe; deep white matter).
4. Candidate formation per hemisphere: gray-band tissue in the medial wall
   of the inferior horn, extracted slice by slice within a search box
   declared in the run script, connected along the rostrocaudal span
   between the registered rostral and caudal limits.
5. Clean: keep the single largest component per hemisphere; report dust
   fraction.

### QC gates (all must pass; failure = reported as failed, not rescued)

- (a) Overlay renders in coronal, axial and sagittal planes eyeballed: the
  mask forms a bilateral lamina in the medial wall of the inferior horn, no
  spill into the ventricular lumen, no extension into lateral temporal
  neocortex, no midline crossing.
- (b) Exactly two main components (one per hemisphere); dust < 2% of total.
- (c) L/R volume ratio inside 0.5–2.0. (Report-only band: outside it
  triggers re-inspection and a declared verdict, never silent symmetrization
  — the rhino lesson.)
- (d) Sanity band, declared in advance: total volume inside **0.3–2.0 cm³**
  for the bottlenose specimen. Basis: Montie et al.'s 1.73 cm³ at Vb
  1,267.57 scaled to 515.46 at the registered slope gives ≈0.81 cm³; the
  registered line at 515.46 predicts 4.33 cm³ and the literature cluster
  (−81 to −92%) maps to 0.35–0.82 cm³. A result outside the band triggers
  re-inspection; if the anatomy genuinely reads otherwise, the value is
  reported with the discrepancy declared, not edited toward the band.
- (e) Uncertainty: ±1-voxel boundary sensitivity (felid Test-B machinery)
  reported with every volume.

### Placement and registered expectation (fixed)

- Residual vs the registered line at the specimen's own denominator
  (515.46 cm³ → predicted 4.33 cm³), and, declared as a second denominator
  choice, at the species-typical Vb 1,476.83 (predicted 10.53). Both
  printed; neither pooled with histology.
- **Registered expectation:** if the cetacean pattern holds in the MRI
  class, the own-denominator residual lands between **−70% and −95%**. A
  residual within ±25% of the line would contradict the literature cluster
  in the same method class as Montie's point; a residual below −95%
  (< 0.22 cm³) would indicate under-delineation and trigger gate (d)
  re-inspection.
- The new points are **not** added to the registered fit set (no refitting,
  §6). They are reported as delineations in the MRI class alongside it.

---

## Item 2 — Rhino confirmatory re-delineation (registered test of a fixed prediction)

### The prediction under test (already fixed in the record)

`REPORT.md` addendum 2026-11-17 §(f), written before any such run:
re-delineating the catalogue black-rhino MRI under one declared tight MRI
protocol (Patzke/Bhagwandin criteria) is predicted to give **≈4.2 cm³** —
on the registered line (predicted 3.80 cm³ at brain 442.65; 4.2 = +10.5%).
Reference values: catalogue label **6.854 cm³**; Patzke compilation
(histology class) **7.48 cm³** at Vb 512.55; Bhagwandin et al. 2017 MRI
tracing **4.71 cm³** on a specimen of identical brain mass (531 g), scaled
to this specimen (×0.883 at the registered slope) ≈ 4.16 cm³.

### Tight criteria (fixed; operationalization of Bhagwandin et al. 2017)

Bhagwandin et al. traced the hippocampus on MRI "using the methodology of
Patzke et al. (2015)" and state its topography: temporal pole caudal to the
amygdaloid complex, amygdala and temporal horn separated by an incursion of
the lateral ventricle; a vertical ventral portion lateral to the diencephalon
turning forward into a dorsal portion lying over the diencephalon. Neither
paper prints slice-level rules, so the tight protocol is operationalized
here, explicitly, as:

- **T1.** Include only the MRI-identifiable hippocampal formation
  (dentate gyrus + cornu ammonis + subiculum) — the gray lamina as it
  appears on the scan.
- **T2.** Rostral boundary at the temporal pole **caudal to the amygdaloid
  complex**, the ventricular incursion as separator. Any label tissue
  rostral of that plane, or continuous with the amygdala, is excluded.
- **T3.** Exclude the fimbria/fornix white-matter thread beyond the alveus
  (the catalogue label carries a thin anterior thread, ax1 < 140,
  0.031 cm³ — a declared exclusion class, however small).
- **T4.** Exclude non-contiguous dust (components other than the two main
  bilateral components; catalogue dust = 0.074 cm³).
- **T5.** Both the ventral vertical portion and the dorsal portion over the
  diencephalon are hippocampus (Bhagwandin's description) and are included.
- **T6.** Execution is a **fresh delineation from the MRI**, not a
  morphological erosion of the catalogue label: slice-by-slice in the
  coronal plane within a search region = the catalogue label's bounding
  extent dilated by 2 voxels, keeping gray-lamina tissue under T1–T5, with
  overlay QC eyeballed in three planes. The catalogue label serves only to
  define the search region and as the comparison value.
- **T7.** Hemispheres traced under identical rules and reported separately
  (catalogue label: L 2.431 / R 4.424 cm³ — the asymmetry is part of what
  the test examines; no symmetrization).

### Decision bands (fixed in advance)

- Result in **3.57–4.83 cm³** (4.2 ± 15%) → **CONFIRMED**: a tight MRI
  tracing reproduces the prediction; the delineation-definition mechanism
  of the rhino investigation is demonstrated, not just inferred.
- Result **≥ 5.48 cm³** (within 20% of the catalogue label) → **REFUTED**:
  an honest tight tracing reproduces the label; the definition mechanism
  fails and the residual reopens.
- Between → **INDETERMINATE / partial**: report the decomposition (which
  exclusion classes carried how much volume) and claim neither verdict.
- Uncertainty reported: ±1-voxel boundary sensitivity on the new tracing.

---

## Item 3 — Ferret residual forensics (declared plan; verdict remains POST-HOC)

The ferret residual (+70.7%: label 0.173 cm³ vs 0.101 cm³ predicted at brain
6.13 cm³) was registered unexplained in `PREDICTION.md` §5 and has never been
investigated. Per §5, any explanation is post-hoc; declaring the sequence in
advance disciplines the forensics but does not change that status. Sequence
(the rhino investigation's, applied in order):

- (a) **Label integrity, round 2:** per-side volumes (not centroids), fill
  fraction of the label's bounding box, component census, position overlays
  eyeballed, header/affine integrity vs the MRI, metadata-swap check against
  the `outputs/label_forensics.csv` patterns (sloth-bear one-sidedness,
  giraffe unilaterality, kangaroo header copying).
- (b) **Denominator:** the 6.13 cm³ in the fit is an Otsu mask (the ferret
  folder has no Atlas mask; the cat's Otsu denominator is known-poisoned).
  Recompute the Otsu sensitivity band; compare against literature brain
  volume/mass for *Mustela putorius furo*; recompute the residual across
  the band.
- (c) **Literature:** the Patzke et al. 2015 compilation carries **no**
  *Mustela putorius* row (verified against the full Table 1 on 2026-11-17:
  its only mustelid rows are *Mustela nivalis*, Vh 0.17 cm³ at Vb 1.45,
  source Reep 2007) — so no compilation value exists to compare; search for
  any other published ferret hippocampus volume and report what exists.
- (d) **Form-failure assessment:** the §3 benchmark's post-hoc diagnosis
  showed the power-law form failing where hippocampal share climbs
  (8–11% at brains < 2 cm³; size-band median APE 69.0% at 2–20 cm³). The
  ferret (brain 6.13, share 2.82%, smallest brain in the n = 8 fit set)
  sits at the fit range's lower edge: assess whether +70.7% is inside the
  line's demonstrated error envelope for its size band, and what Patzke's
  saturating-exponential model (the gradeable comparator) predicts at
  6.13 cm³.
- **Verdict classes (one, chosen on the evidence):** label artifact /
  denominator / definition mismatch / form failure / genuine residual.
