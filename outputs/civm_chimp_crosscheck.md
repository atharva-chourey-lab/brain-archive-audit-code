# CIVM → chimpanzee hippocampus cross-check — **1.56 cm³; D99's 1.48 corroborated**

**Date:** 2026-11-17 · **Script:** `scripts/civm_chimp_crosscheck.py` ·
**Label:** `outputs/segmentations/Chimpanzee_hippocampus_CIVM_propagated.nii.gz` ·
**QC:** `outputs/segmentations/qc_chimpanzee_hippocampus_CIVM.png` (viewed)

## Result

| Estimate | Value | Source |
|---|---|---|
| **CIVM propagation (this run)** | **1.56 cm³** | CIVM label 79 ("Hip") → chimp MRI, 1 mm affine |
| D99 propagation (earlier) | 1.48 cm³ | D99 formation labels → same chimp MRI, same pipeline |
| Modern stereology (literature) | 1.77 cm³ | published value |

CIVM sits **+5.4% above D99** and **−12% below stereology** — squarely in the
pre-set "supports the D99 number" band (~1.4–1.6). It rules out the alternative
the cross-check was built to test: a ~2.5 cm³ outcome would have indicted the
D99 propagation as shrunk/misplaced. An independent atlas, independent pipeline,
same scan → essentially the same number. The chimp propagated point (flagged
PROVISIONAL since the D99 run) is upgraded to **corroborated as an affine-
propagation estimate**.

## Method (identical recipe to the D99 run)

Project convention, mirrored exactly from `scripts/segment_primates.py`: atlas =
registration static, subject = moving; both sides coarsened to ~1 mm; dipy mutual-
information affine (translation → rigid → affine, level_iters [200, 100, 25]);
labels pulled into subject space with `transform_inverse`, nearest-neighbour;
volume on the 1 mm subject grid. Inputs: CIVM b0 + labels from
`goldmine-hunter/gold/sba-macaque/` (SBA template CBCetal15, Calabrese et al.
2015); hippocampus = **label 79** per the SBA's own key
(`outputs/civm_label_key_hunt.md`); subject = Brain Catalogue chimpanzee
MRI-n4 masked with its Atlas mask — the same scan the D99 run used.

## QC (overlay viewed, three planes, both components)

- **Placement: PASS.** The label forms two coherent components (774 + 753 vox;
  remainder ≤8 vox NN specks) in bilateral medial-temporal territory, tracing
  the expected hippocampal arcs. The specimen sits tilted in its grid, which
  the affine follows.
- **Cross-atlas agreement:** centroids 3.1 vox apart (CIVM [54.1, 38.0, 19.6]
  vs D99 [55.4, 40.5, 21.3]); on slice after slice the red (CIVM) and blue (D99)
  arcs run adjacent/interleaved along the same curve. Dice 0.146 — low in
  absolute terms because two thin arcs offset by 2–4 vox overlap little; this
  is *not* a wrong-territory landing (contrast felid Test A: Dice 0.000/0.001,
  centroids 16–33 mm off, labels in wrong territory, declared VOID).
- Template-side sanity: CIVM rhesus hippocampus 0.641 cm³ in a 74.3 cm³
  labelled brain; the chimp propagation scales it ×2.4, in family with the
  D99 result.

## Caveats (standing, declared)

- **Both values are affine propagations.** Agreement between them cannot
  exclude a shared method bias — affine-only warps plausibly underestimate a
  curved structure, which may be part of the remaining ~12–16% gap to the
  1.77 cm³ stereology value. What the cross-check excludes is a *D99-specific*
  artifact, not propagation bias in general.
- **CIVM is a foreign pipeline** (Calabrese et al. 2015, Duke CIVM via SBA).
  This number is cross-check material only; it is **not pooled** into the
  project's allometric fits, per the standing rule.
- One subject scan, n=1, ex vivo — same limits as the D99 point it checks.

## Transparency note

A first execution of the script flipped the static/moving assignment relative
to the project convention and produced 0.18 cm³ on the template grid — a
scripting error in this run, caught because the output grid and lopsided split
betrayed it, and discarded. The rerun mirrors `segment_primates.py` exactly;
no method was changed, tuned, or rescued — the registered cross-check is the
project's standard pipeline, run once, as specified.
