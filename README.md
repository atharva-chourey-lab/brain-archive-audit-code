# Brain Archive Audit — Code

**Code for the "Lost Atlas" brain-scan comparison: a voxel-level audit of
published brain-atlas labels, and the first MRI measurement of the lion
hippocampus.**

Manuscript: https://github.com/atharva-chourey-lab/lost-atlas

## What this code does

- **Label forensics** (`scripts/label_forensics.py`, `scripts/inspect_lion.py`):
  loads atlas label volumes and checks whether a named structure's label is
  actually present and non-empty — the audit that found both published dolphin
  hippocampus labels to be empty placeholders.
- **Segmentation and volumetry** (`scripts/segment_*.py`,
  `scripts/volumetry_*.py`, `scripts/make_measurements.py`): delineates the
  hippocampus in lion, felid, primate, wallaby, wolf and human scans and
  computes volumes in cm³.
- **Blind benchmark** (`scripts/benchmark.py`): scores the lab's delineations
  against published histological compilation values under the pre-registered
  protocol in `PREDICTION.md` (median APE 66.0% vs the 18.2% reference).
- **Cross-species tables** (`scripts/cross_species_table*.py`): builds the
  paired histology-vs-MRI comparison behind the "~1.6× Two Rulers" result.
- **Rhino anomaly investigation** (`scripts/rhino_*.py`,
  `scripts/delineate_rhino_hippocampus_tight.py`): the follow-up that reopened
  the rhino case, under `PREREGISTRATION_rhino_anomaly_2026-11-17.md`.
- **Aquatic extension** (`aquatic/scripts/`): measurement and analysis for
  cetacean scans, including the bottlenose-dolphin delineation attempt that
  failed QC (no volume is claimed for it — see `outputs/dolphin_delineation.md`).

Key outputs are committed under `outputs/` (CSV/JSON/Markdown only).
`REPORT.md` and `BENCHMARK.md` record the full results.

## How to run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # nibabel, nilearn, numpy, pandas, scipy, scikit-image, matplotlib
python3 scripts/label_forensics.py
python3 scripts/benchmark.py
```

## Data — not redistributed

The MRI scans themselves (~1.9 GB of NIfTI/surface files from M-CRIB, the Brain
Catalogue, CIVM/SBA atlases and others) are **not** in this repository: they
belong to their source archives and are too large for git. Download them from
the original archives; `data/PROVENANCE_human_infant.md` records provenance for
the human-infant set, and `REPORT.md` names every dataset used. Scripts expect
the scans in a local `data/` tree (see each script's header). One script
(`scripts/civm_identify_hippocampus.py`) reads the macaque atlas path from the
`SBA_MACAQUE_DIR` environment variable.

## Status

Research code as run for the manuscript — not a packaged library. Scripts are
ordered by the analysis pipeline, not refactored for reuse; paths and dataset
layout follow the headers in each file. All headline numbers in the manuscript
trace to the committed outputs.

## Authorship and licence

**Author:** Atharva Chourey, Atharva Chourey Lab (independent research lab)

The Atharva Chourey Lab is a human–AI collaboration: Atharva Chourey works with
Lapis (Muse), an AI research partner. All results are framed as the
collaboration's.

Code in this repository is released under the **MIT License** (see `LICENSE`).
The associated manuscripts are published separately under CC BY 4.0 — the code
licence and the paper licence are deliberately different.
