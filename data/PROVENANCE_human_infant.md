# Human infant MRI — provenance & dataset landscape

Compiled 2026-11-16 (America/Los_Angeles). All access claims below were verified
live on this date via the repositories' own pages/APIs. No registration,
paywall, or credential was used or bypassed for anything in this folder.

---

## 1. What was downloaded (the best OPEN option)

**M-CRIB 2.0 neonatal brain atlas dataset** — Melbourne Children's Regional
Infant Brain atlas (Alexander et al., *Frontiers in Neuroscience* 2019,
doi:10.3389/fnins.2019.00034; original M-CRIB: Alexander et al., *NeuroImage*
2017, doi:10.1016/j.neuroimage.2016.09.068).

- Repository: Open Science Framework (OSF), node `4vthr`
  - Project page: https://osf.io/4vthr/
  - File API used: https://api.osf.io/v2/nodes/4vthr/files/osfstorage/
- Access: **fully open** — direct anonymous HTTPS download per file
  (`https://osf.io/download/<file-guid>/`), no account, no agreement.
- License: no license field is set on the OSF node metadata (checked via API);
  the companion M-CRIB-WM release (Alexander et al., *Hum Brain Mapp* 2020)
  states its OSF data are CC BY 4.0. Cite Alexander et al. when using.
- Cohort: **10 healthy term-born neonates** (4 F / 6 M), GA at birth
  38.1–42.0 wk, **PMA at scan 40.3–43.0 wk (mean 41.7)** — see
  `mcrib2/M-CRIB_atlas_demographic_info.csv`.
- Acquisition (from Alexander et al. 2019): 3 T; T2w transverse turbo spin
  echo, 1 mm slices, in-plane 1 mm² zero-filled to 0.5 mm; T1w also acquired.
  Distributed preprocessed images are bias-corrected, skull-stripped,
  AC-PC aligned, resampled **0.63 mm isotropic** (parcellation/T2 space).
- Parcellation: **94 regions** (Desikan-Killiany-Tourville-compatible cortical
  labels ≥1000 + FreeSurfer-style subcortical labels), manually traced/edited —
  the reference standard for neonatal volumetry. Label lookup:
  `mcrib2/labels/M-CRIB_2-0_labels_itk_format.txt`.

### Files downloaded (32 files, 140 MB total, 2026-11-16)

Folder `mcrib2/subjects/` — for **each of P01–P10**:
`M-CRIB_<P>_T2.nii.gz` (preprocessed T2w), `M-CRIB_<P>_T1.nii.gz`
(preprocessed T1w), `M-CRIB_2-0_<P>_parc.nii.gz` (94-region parcellation).
Plus `mcrib2/labels/M-CRIB_2-0_labels_itk_format.txt` and
`mcrib2/M-CRIB_atlas_demographic_info.csv`.
Not downloaded (still openly available at the same node): raw T1/T2,
T1-registered-to-T2 copies — redundant for volumetry.

Exact per-file download URLs (OSF file GUIDs):
- Labels: https://osf.io/download/9u42m/ · Demographics: https://osf.io/download/mzhcr/
- Parcellations P01–P10: m59ug, g94dv, zbav3, pg8ch, cqp4w, 2tw38, rb3vc, f5wrd, kz49t, u5nqr
- T2 P01–P10: mpcrg, a4g2p, ue8sa, hf8qz, frqxt, ge2f4, f953u, ufjm2, f38et, aunhe
- T1 P01–P10: yz938, e34wg, tf2rx, hxsgz, jm4ut, xt23u, fqw45, 586am, fv4tq, kc8zs
  (each as https://osf.io/download/<guid>/)

### Validation (nibabel 5.5.0, 2026-11-16)

All 30 NIfTI files load cleanly.
- Parcellations: 304×304×157, 0.63 mm iso, uint16, **94 labels in every subject**.
- T2: 304×304×157, 0.63 mm iso, float32 (same space as parcellations).
- T1: 348×384×128, 0.5×0.5×1.0 mm, float32 (native space).

### Cohort volumetry computed from these parcellations (voxel count × 0.63³ mm³)

Mean ± SD across the 10 neonates (cm³). NOTE: the M-CRIB "CSF" label (24)
includes extra-axial CSF inside the traced mask and varies widely
(74–141 cm³); **tissue-only total ≈ 374 cm³** is the figure comparable to
published "total brain volume".

| Region | Mean cm³ | SD | Range |
|---|---|---|---|
| All labelled voxels (incl. CSF+ventricles) | 474.0 | 43.5 | 420.8–553.1 |
| Cortical gray matter (DKT labels ≥1000) | 160.9 | 19.0 | 139.8–207.4 |
| Cerebral white matter (2+41) | 161.1 | 14.1 | 141.8–194.4 |
| CSF label (24) | 93.5 | 18.6 | 74.0–140.9 |
| Cerebellum (75,76,90,91,93) | 23.4 | 3.0 | 19.1–29.1 |
| Thalamus (9+48) | 7.8 | 0.8 | 6.8–9.0 |
| Brainstem (170) | 5.4 | 0.6 | 4.5–6.2 |
| Ventricles (4,14,15,43) | 6.1 | 1.5 | 4.4–9.9 |
| Putamen (12+51) | 3.5 | 0.3 | 3.1–3.9 |
| Hippocampus (17+53) | 2.9 | 0.3 | 2.4–3.7 |
| Caudate (11+50) | 2.7 | 0.3 | 2.3–3.2 |
| Ventral DC (28+60; incl. hypothalamic region) | 2.4 | 0.2 | 2.1–2.9 |
| Amygdala (18+54) | 1.64 | 0.17 | 1.39–1.91 |
| Pallidum (13+52) | 1.55 | 0.16 | 1.2–1.8 |
| Corpus callosum (192) | 0.76 | 0.18 | 0.5–1.0 |
| Accumbens (26+58) | 0.38 | 0.06 | 0.3–0.5 |

Method note: M-CRIB 2.0 does not separate hypothalamus or periaqueductal gray
as standalone labels; the closest label is Ventral DC (28/60). No dMRI or fMRI
is distributed with M-CRIB — structural T1/T2 only.

---

## 2. Dataset landscape — open vs gated (verified 2026-11-16)

| Dataset | Access | N / ages | Modalities | Labels? | URL |
|---|---|---|---|---|---|
| **M-CRIB 2.0** (OSF) | **OPEN** (downloaded) | 10 term neonates, PMA 40–43 wk | T1w, T2w | Yes — 94-region manual parcellation/subject | https://osf.io/4vthr/ |
| **M-CRIB-WM** (OSF) | **OPEN**, CC BY 4.0 | Same 10 neonates | T1w, T2w, DEC (diffusion-derived) | Yes — 54 WM regions; combined M-CRIB-WM+2.0 = 148 regions | https://osf.io/mnwv9/ |
| **Baby Open Brains (BOBs)** = OpenNeuro **ds005450** | **OPEN** (OpenNeuro/S3 anonymous; also S3 mirror bobsrepository.s3.amazonaws.com) | 51 infants, **71 visits, 1.0–9.4 months** (NOT newborn; mean 5.3 mo), Siemens 3T Prisma | T1w (MPRAGE), T2w | Yes — 31 expert-corrected segmentation labels/visit, BIBSNet protocol | https://openneuro.org/datasets/ds005450/ · paper: Feczko et al., Sci Data 2025, doi:10.1038/s41597-025-05404-y · OSF hub doi:10.17605/OSF.IO/WDR78 |
| **dHCP** (Developing Human Connectome Project), Release 3 | **GATED** — two historical/current gates, see §3 | 783 neonates (886 datasets), 20–44 wk PMA; +273 fetal | T1w/T2w, dMRI, rs-fMRI + pipelines incl. segmentations | Yes (pipeline derivatives) — behind the gate | https://biomedia.github.io/dHCP-release-notes/ |
| **ALBERTs** (Gousias et al. 2012) via Brain Development (Imperial) | **REGISTRATION** (catalogued as registration-required; form on brain-development.org) | 20 neonates (15 preterm-at-term + 5 term) | T1w, T2w | Yes — 50 ROIs/subject | https://brain-development.org/brain-atlases/neonatal-brain-atlases/ |
| **Makropoulos et al. neonatal atlas (87 structures)** via Brain Development | Direct zip link published on the atlas page (no registration mentioned); binary not fetch-verified here | Probabilistic/max-probability 4D atlas built from 420 neonatal MRIs, weekly templates ~37–44 wk | T1/T2 templates + 87-structure probability maps | Yes — atlas-space labels (not individual subjects) | https://brain-development.org/?p=173 (download: NeonatalStructuralAtlas.zip, doc.ic.ac.uk) |
| **dHCP volumetric atlas** (Schuh et al.) | Hosted on GIN (git-annex); anonymous HTTPS not verified — GIN unreachable in our test window | Groupwise spatiotemporal volumetric atlas, 28–44 wk | T2w templates + tissue/structure probability maps | Yes | https://gin.g-node.org/BioMedIA/dhcp-volumetric-atlas-groupwise |
| **UNC Infant 0-1-2 Atlases** (Shi et al. 2011) | Free download via UNC IDEA / NITRC (CC Attribution per SciCrunch record) | Atlases built from 95 infants scanned as neonates, 1 yr, 2 yr | T1/T2 intensity templates | Yes — tissue probability maps + anatomical parcellation map per age | https://www.nitrc.org/projects/pediatricatlas · RRID:SCR_002569 |
| **UNC detail-preserved longitudinal infant atlases** (Zhang et al. 2016, NITRC) | Free via NITRC | Templates at 0, 3, 6, 9, 12 months | T1w + T2w atlases, NIfTI | Probabilistic segmentation maps | https://www.nitrc.org (search "infant atlas") |
| **Zenodo** (searched: neonatal/newborn brain MRI + segmentation) | — | **No human newborn structural MRI + segmentation dataset found.** Hits: LISA low-field pediatric segmentation challenge (description PDF only on Zenodo; data via challenge), FaBiAN *synthetic fetal* MRI (doi:10.5281/zenodo.6477946), animal datasets | — | — | https://zenodo.org |

"Melbourne neonatal atlas" in the task list **is** M-CRIB (Melbourne
Children's Regional Infant Brain) — same resource, not a separate one.

## 3. The dHCP gate, precisely

dHCP subject data are **not** openly downloadable without an agreement:
- Current route (Release 3): via the NIH **NDA, collection 3955**. Requires
  (1) an NDA user account + login.gov, (2) approved **data access permission**
  (institutional signing official + Data Access Committee review), then
  download via the NDA Download Manager. Source: dHCP "Guidelines for
  downloading data from the NDA" at https://biomedia.github.io/dHCP-release-notes/
- Legacy route (developingconnectome.org): registration with an **institutional
  email** (personal email explicitly not accepted), then signing the dHCP
  **Data Sharing Agreement / Open Access Terms of Use** per dataset before
  download unlocks (academic torrent or HTTPS).
- What IS open without any gate: release notes, pipeline code
  (github.com/BioMedIA), the combined demographics TSV, and derived
  tractography-ready diffusion files mirrored at brain.labsolver.org —
  but those mirrors still state the dHCP Data Sharing Agreement applies.
- Derived-data mirror warning: the GitHub `data-hcp/lifespan` repo distributes
  dHCP *derived diffusion* files under the dHCP agreement — not a loophole.

## 4. Literature fallback values — term newborn brain volumes

For cross-checking / if subject-level data are ever unusable. All values are
**measured** (not computed by us) from the cited cohorts:

**Wu et al., JAMA Pediatrics 2025** (doi:10.1001/jamapediatrics.2025.0277) —
OBOE study, 96 unexposed term-newborn controls, 3D volumetric MRI <8 wk,
mean PMA at scan 42.84 wk:
- Total brain volume **407.06 cm³**
- Cortical volume **176.35 cm³**
- White matter **166.65 cm³**
- Deep gray matter **28.76 cm³**
- Cerebellum **24.99 cm³**
- Brainstem **7.18 cm³**
- Amygdala: left **0.51 cm³**, right **0.55 cm³** (≈1.06 total — smaller than
  M-CRIB's 1.64; different segmentation protocol — MANTiS-style vs manual
  DKT/FreeSurfer labels. Protocol differences of this size are normal for
  small structures and must be reported, not averaged away.)

Consistency check: our M-CRIB tissue-only total (≈374 cm³ at mean PMA 41.7 wk)
sits plausibly below Wu et al.'s 407 cm³ at PMA 42.8 wk given ~1 wk less
maturation and different tissue-class definitions (M-CRIB cortical GM excludes
some subcortical/WM boundary tissue counted elsewhere). The two sources agree
to within expected protocol/age differences on WM (161 vs 167), cerebellum
(23.4 vs 25.0), and cortical GM (161 vs 176).

## 5. Gaps relevant to the comparison project

- **No openly downloadable human newborn dMRI or rs-fMRI with segmentations**
  was found: newborn diffusion/functional data exist openly only inside dHCP
  (gated, §3). BOBs (open) is structural-only and 1–9 months old.
- M-CRIB-WM (open, OSF mnwv9) adds diffusion-derived DEC maps + 54 WM-region
  parcellations for the same 10 neonates — the closest open proxy for
  white-matter organization at term.
- Hypothalamus and periaqueductal gray are **not separately labelled** in any
  open neonatal atlas found (M-CRIB's Ventral DC is the nearest label).
