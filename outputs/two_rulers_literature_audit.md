# The Two Rulers — Literature Audit

**Question:** How established is the histology-vs-MRI volumetric offset (histology/stereology
hippocampus volumes running systematically larger than MRI-segmentation volumes at the same
brain size), and what is the most prestigious place it is stated or used?

**Project claim under audit:** across 343 species, hippocampus volumes from the
Stephan/Reep/Patzke histological tradition run ~1.6× larger than an MRI-label allometric line
at the same brain size; on one black rhino specimen the same lab (Manger's) published
7.48 cm³ (compilation, histology definition; Patzke et al. 2015) vs 4.71 cm³ (MRI;
Bhagwandin, Haagensen & Manger 2017) — a 1.59× discrepancy on a single brain.

**Method:** every item below was verified by opening the source (full text unless flagged).
Searches were targeted (histology-vs-MRI volumetry, shrinkage correction, the
Stephan/Patzke/Manger corpus, prestige venues), not an exhaustive systematic review;
novelty statements are hedged to that coverage.

---

## 1. Count and roster

**Counting rule:** a "place" = a publication in which the offset (or its shrinkage-correction
mechanism) is explicitly quantified with a number, or operationally applied as a numbered
correction. Under that rule: **14 verified items** — 3 direct cross-method quantifications,
6 processing-shrinkage quantifications, 2 methods-authority statements, 3 delineation-class
items (the offset's second mechanism). No item is counted twice.

### A. Direct histology-vs-MRI quantifications

1. **Navarrete et al. 2018, *Brain, Behavior and Evolution* 91:109–117** — the closest prior
   work to this project. MRI measurements of 39 primate species (53 brains) compared against
   the Stephan et al. serial-section dataset; 17 species with both. Percent errors (positive =
   serial-section/histology value larger): total brain +3.5%, telencephalon −4.5%, cerebellum
   +8.2%, diencephalon +3.1%, neocortex +18.1%, striatum +22.1%, **hippocampus +31.5%
   (range 13.1–59.6) — the largest discrepancy of any structure**, mesencephalon +23.5%,
   medulla+pons −13.3%. (Percent-error denominator convention is not fully specified in the
   text; the hippocampus ratio is ≈1.3–1.46× depending on convention.) Attribution:
   differential shrinkage — "we, like Stephan et al. [1981], assume that shrinkage affects all
   brain areas equally, which may not be the case"; datasets may be combined only "while
   taking dataset differences into account"; techniques should ideally be compared "on the
   same brains directly." The paper also reports MRI volumes running a mean −9.1% below
   pre-storage brain volumes (preservation effect).
2. **Delgado-González et al. 2015, *PLoS ONE* 10(6):e0130314** — the same 12 human brains
   measured by ex vivo MRI and by histology (frozen sections). Hippocampus: histology > MRI in
   all four hemisphere × age-group cells (3.62 vs 3.15; 4.54 vs 2.30; 3.68 vs 2.72; 3.33 vs
   2.92 cm³); pooled ratio ≈ **1.37×** (our computation from their published Tables 3–4).
   Temporal lobe volume +13% for histology overall; method difference significant mainly for
   the hippocampus (ANOVA p<0.01). Attribution: clearer boundary identification in histology
   plus MRI partial-volume effects — **delineation, not shrinkage correction** (frozen
   sections; no upward correction applied, yet histology still read larger).
3. **Bobinski et al. 2000, *Neuroscience* 95:721–725** — postmortem MRI vs histological
   hippocampal volumes, 15 human cases; "after controlling for shrinkage," correlations
   r = 0.97 (hippocampus), 0.95 (hippocampus/subiculum), 0.89 (hippocampus/parahippocampal
   gyrus). **No absolute ratio stated.** *(Verified at abstract level only.)*

### B. Processing-shrinkage quantifications (the correction-factor mechanism)

4. **Quester & Schröder 1997, *Journal of Neuroscience Methods* 75:81–89** — fresh human
   brains (n=33): formalin fixation changed brainstem length −1 to −8% (correction factors
   1.01–1.09); paraffin embedding shrank tissue 11–12% linearly (transverse) and 17%
   (longitudinal), factors 1.12–1.21; cerebrum embedding shrinkage 11–25% linear in the cited
   literature (factors 1.13–1.34) — i.e. volumetric corrections up to ~2.4×.
5. **Elias & Schwartz 1971, *Zeitschrift für Säugetierkunde* 36:147–163** — calf brains:
   formalin fixation ≈0.9% mean volume change for whole brains (~13% for blocks);
   paraffin/celloidin embedding shrinkage **~41% by volume** (correction factor ≈1.7); the
   authors therefore measured wet fixed specimens and corrected the one embedded specimen.
6. **Wehrl et al. 2015, *Histology and Histopathology* 30:601–613** — mouse whole brain,
   in vivo MRI baseline vs fixation + dehydration + paraffin embedding: volume shrinkage
   68.1% (PLP), 60.2% (PFA), 58.6% (neutral-buffered formalin), 33.5% (zinc-based fixative) —
   implied correction factors ~1.5–3.1×.
7. **Yeung et al. 2014, *Cell*** — human corpus callosum stereology (n=55): "a total volume
   shrinkage of 32.2% ± 9.5%," measured and corrected individually per subject (factor
   ≈1.47), following Dorph-Petersen, Nyengaard & Gundersen 2001, *J Microsc* 204:232–246
   (the z-shrinkage estimation standard; cited within Yeung et al., not independently opened).
8. **Wagstyl et al. 2020, *PLoS Biology* 18(4):e3000678**, on the BigBrain specimen
   (Amunts et al. 2013, *Science* 340:1472–1475): "a volume-based (3D) shrinkage factor of
   **1.931**" — fresh volume (inferred from fresh weight) vs volume after histological
   processing; per-axis scale factors from coregistration to an MRI template 1.15 / 1.22 /
   1.43. Histology surfaces are explicitly transformed "for comparison to in vivo measures."
9. **Amunts et al. 2005, *Anatomy and Embryology* 210:343–352** — the Julich cytoarchitectonic
   atlas of the human amygdala, hippocampal region and entorhinal cortex: every reported
   volume carries a per-brain shrinkage factor F, "defined as the ratio between the estimated
   fresh volume of the brain and its volume after histological processing," because "in order
   to estimate the true volumes, shrinkage due to histological processing has to be taken into
   account." Shrinkage-corrected hippocampal totals: 4,713 ± 1,007 mm³ (left),
   4,884 ± 1,087 mm³ (right) — on the broad cytoarchitectonic definition (incl. subiculum and
   HATA), so not directly ratio-able against MRI protocols; counted as operational use, not
   as a cross-method comparison.

### C. Methods-authority statements

10. **Schmitz & Hof 2005, *Neuroscience* 130:813–831** — the design-based stereology field's
    standard guidance: group comparisons should be restricted to tissue processed the same
    way, and z-axis shrinkage during histology must be measured and taken into account when
    estimating in-situ volume. *(Verified via stereology.info's detailed review summary of
    the paper, not the full text.)*
11. **Healy & Rowe 2007, *Proceedings of the Royal Society B* 274:453–464** — a critique of
    comparative brain-size studies: "brains of different species or genera may shrink or
    re-hydrate to different extents"; "different ways of measuring whole brain size do not
    always result in the same outcome"; combining data "produced from different studies using
    different methods, without clearly demonstrating that this is appropriate," is flagged as
    a rigour failure — "it seems curious that checking for potential biases is rarely, if
    ever, carried out." A warning about method-mixing, not a quantification.

### D. Delineation class (the offset's second mechanism — within MRI)

12. **Boccardi et al. 2011, *Journal of Alzheimer's Disease* 26(Suppl 3):61–75; Boccardi et
    al. 2013, *Alzheimer's & Dementia*** — 12 published MRI hippocampal segmentation protocols
    produce **up to 2.5-fold** volume differences on the same scans. This discrepancy is the
    stated motivation for the EADC-ADNI Harmonized Protocol (HarP; validation: Apostolova et
    al. 2015, *Alzheimers Dement* 11:139–150).
13. **Navarrete et al. 2019 (erratum), *Brain, Behavior and Evolution* 92:182–184** — the
    authors' own MRI hippocampus values were consistently *lower* than Sherwood et al. 2004's
    MRI dataset: mean percent error 35.8% (range 20.0–46.9%), n=5 species. Delineation-criteria
    differences of ~36% exist even with the method held constant.
14. **The comparative tradition's own normalization practice** — as described in the LGN
    scaling literature (J Comp Neurol 2014;522:1839–1857, on the Chalfin et al. 2007 method):
    "the volume of the entire fresh brain was divided by the volume of its serial-section-
    reconstructed counterpart to obtain a shrinkage correctional factor, and this was
    applied" to structure volumes, with brain specific gravity 1.036 (Stephan et al. 1981).
    Reep et al. 2007 (per this project's BENCHMARK.md) used species-specific factors for six
    taxa and a mean factor of 2.4 for the rest. *(Verified via the citing paper's text.)*

*Not counted:* Isler et al. 2008 and Iwaniuk & Nelson 2002 (endocranial volume vs brain
volume — a different ruler pair); Adler et al. 2014, *NeuroImage* (histology-derived
hippocampal subfield annotation in postmortem MRI — no offset ratio; note it is *NeuroImage*,
not *Neuron*).

---

## 2. Most prestigious instance

**No statement of the composite claim** — "the histological comparative record reads ~1.6×
larger than the MRI record for the hippocampus" — **was found in Nature, Science, PNAS,
Neuron, Nature Neuroscience, or any Annual Review.** In top-tier venues, only the components
appear.

**The single most prestigious concrete instance: the BigBrain shrinkage factor.**
Amunts et al. 2013, *Science* 340:1472–1475 ("BigBrain: An Ultrahigh-Resolution 3D Human
Brain Model") built the field's flagship histological brain model by reconstructing 7,404
histological sections against MRI/blockface references precisely because histological
processing distorts and shrinks tissue. The exact quantified claim, published in the model's
methods follow-up (Wagstyl et al. 2020, *PLoS Biology* 18(4):e3000678): the specimen's
**volume-based (3D) shrinkage factor is 1.931** — the processed histological volume must be
multiplied by ~1.93 to recover the fresh volume inferred from fresh weight — with anisotropic
per-axis corrections of 1.15 / 1.22 / 1.43 against an MRI template. Honest caveat: the numeral
1.931 lives in the *PLoS Biology* paper, not in *Science* itself.

Runner-up, and the largest shrinkage number stated inside a top-tier journal itself:
**Yeung et al. 2014, *Cell*** — 32.2% ± 9.5% total volume shrinkage, measured and corrected
per subject (corpus callosum stereology; frozen-section processing, cell-counting context —
not a histology-vs-MRI volume comparison).

---

## 3. Inside the tradition: acknowledgements — and their absence

- **Patzke et al. 2015, *Brain Structure and Function* 220:361–383** (the 375-species
  compilation at the centre of the project's claim): verified by full-text search of the
  author manuscript — the word "shrink" appears **nowhere** in the paper. The compilation
  pools literature histology values (Pirlot & Nelson 1978; Stephan et al. 1981; Baron et al.
  1996; Reep et al. 2007; Montie et al. 2008) with values "calculated from MRI scans"
  (Manger et al. 2010; Patzke et al. 2013a) in a single regression, with **zero discussion of
  shrinkage or cross-method comparability**.
- **Bhagwandin, Haagensen & Manger 2017, *Frontiers in Neuroanatomy* 11:74** (the MRI rhino
  paper): verified — the value 7.48 cm³ appears **nowhere** in the paper. The authors never
  mention their own compilation's value for the same species/specimen. Instead the MRI values
  are described as "very close to what would be predicted based on regressions derived from
  other mammals, with the black rhinoceros falling within the 95% confidence intervals of the
  mammalian regression… (Patzke et al., 2015)" — agreement with the mixed-method regression is
  treated as validation. **The 1.59× intra-lab discrepancy (7.48 vs 4.71 cm³) is nowhere
  commented on, by its own authors or, in this audit's coverage, by anyone.**
- **Patzke et al. 2014, *Brain Structure and Function* 219:1587–1601** — the one partial
  exception: the elephant hippocampus study was motivated by the observation that "the data
  available regarding hippocampal size of the elephant are inconsistent," and re-measured it
  by MRI (10.84 ± 0.33 cm³). An inconsistency was noticed and re-measured — but no offset was
  quantified and no cross-method comparison stated. *(Verified via the PubMed abstract.)*
- The tradition corrects **within** its own pipeline — whole-brain fresh/sectioned ratios
  (item 14), species-specific factors where measured, a mean factor of 2.4 where not — and
  treats the corrected values as "fresh volumes." It never bridges to MRI. Its corrections are
  also structure-blind (one whole-brain factor applied to every structure), which is exactly
  the assumption Navarrete et al. 2018 flag as questionable.

---

## 4. Scale verdict

The largest direct, paired cross-method quantification found is **Navarrete et al. 2018:
17 primate species × ~8 structures**. Same-specimen human studies are smaller (n=12–15
brains). **No meta-analysis of the histology-vs-MRI offset, and no quantification across
hundreds of species or across a whole literature, was found.** Within the audit's coverage,
the project's 343-species grading of the published record against a single MRI line is the
first quantification at literature scale — with the caveat that it is indirect (published
values vs a fitted line) where Navarrete's is paired (same structures, both methods).

## 5. Terminology verdict

The components have standard names: **"tissue shrinkage," "shrinkage factor" / "shrinkage
correction(al) factor," "z-axis (z-) shrinkage," "differential shrinkage"** (grey vs white
matter shrinking unequally — Kretschmann et al. 1982, via Navarrete et al. 2018), and the
"positive formalin effect" (fixation swelling). **There is no standard name for the composite
offset** between the histological comparative record and the MRI segmentation record. Nobody
in the audited literature calls it anything; "The Two Rulers" is this project's coinage, and
no equivalent term was found.

---

## 6. Novelty assessment (hedged to audit coverage)

**Not novel — do not claim:**
- The existence of the offset. It is quantified in print (Navarrete 2018; Delgado-González
  2015) and its mechanism is textbook-level knowledge in stereology (Schmitz & Hof 2005).
- Either mechanism. Shrinkage correction factors of 1.5–3× are measured and published across
  five decades (Elias & Schwartz 1971 → Wehrl 2015 → Wagstyl 2020), and delineation-criteria
  spreads of up to 2.5× are documented within MRI alone (Boccardi 2011/2013).
- Primate-scale quantification, including the hippocampus being the worst-discrepancy
  structure (Navarrete 2018: +31.5%, p<0.0001).

**Survives as novel (within this audit's coverage):**
- **Whole-literature scale.** Grading 343 species' published values against one MRI line is
  an order of magnitude beyond the largest prior quantification (17 species). Nobody has
  previously put a number on the offset for the comparative record as a whole.
- **The single-specimen demonstration.** One brain, one lab, two published values 1.59×
  apart (rhino: 7.48 compilation vs 4.71 MRI), with the discrepancy never remarked by its own
  authors — verified absence in Bhagwandin et al. 2017. No equivalent same-specimen,
  same-lab, cross-publication demonstration was found.
- **The catalogue definition-mismatch diagnosis.** The rhino investigation's finding — a
  label drawn to a histology-style (broad) definition sitting inside an MRI dataset, reading
  +65% above the tight-MRI expectation but +3.7% above the broad-definition expectation — is
  a distinct failure mode from both classical mechanisms (it is not processing shrinkage and
  not inter-protocol spread within one archive; it is a definition imported across methods).
  Nothing matching it was found in the audited literature.

**One tension the project should state itself:** the project's ~1.6× literature-wide estimate
is larger than Navarrete et al.'s paired hippocampal figure (+31.5%, ≈1.3–1.46×). Plausible
reasons, all consistent with the audited record: the project's comparator is a fitted
allometric line rather than paired measurements; its taxa extend far beyond primates; and the
compilation's default correction (mean factor 2.4 for taxa without measured factors, per
Reep et al. 2007) plausibly inflates the histology side beyond specimen-specific corrections.
The audit strengthens the phenomenon — and suggests the project's point estimate sits at the
high end of it.

*Audit coverage note: targeted searches and full-text verification as flagged per item;
Bobinski 2000 abstract-level; Schmitz & Hof 2005 via a detailed secondary summary;
Dorph-Petersen 2001 cited-within only; Patzke 2014 abstract-level; Healy & Rowe 2007
abstract plus the quoted passage read in full text; Navarrete percent-error denominator
convention hedged as noted; Delgado-González pooled ratio computed by this audit from the
paper's published table values.*
