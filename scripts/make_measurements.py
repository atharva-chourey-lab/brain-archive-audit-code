"""Assemble the master measurements.csv: every value traceable to a computation
in this repo or a cited publication; unavailable metrics are explicit rows."""
import pandas as pd, numpy as np

H = pd.read_csv("outputs/human_volumes_per_subject.csv")
LION_VOL, LION_LO, LION_HI = 188.1, 178.2, 193.4  # Otsu; +/-10% threshold band

rows = []
def add(species, specimen, region, value, unit, norm_value, norm_basis, source,
        method, value_type, confidence, notes=""):
    rows.append(dict(species=species, specimen=specimen, region=region, value=value,
        unit=unit, normalized_value=norm_value, normalization_basis=norm_basis,
        source=source, method=method, value_type=value_type,
        confidence=confidence, notes=notes))

HUM_SRC = "M-CRIB 2.0 (OSF 4vthr), 10 term neonates, PMA 40.3-43.0 wk"
HUM_METH = "voxel count of manual 94-region parcellation labels x voxel volume (this repo: scripts/volumetry_human.py)"
for region, col in [("total_brain_tissue","total_brain_tissue"),
    ("cortical_gray_matter","cortical_gray_matter"),("cerebral_white_matter","cerebral_white_matter"),
    ("frontal_cortex_DKT","frontal_cortex_dkt"),("amygdala","amygdala"),("hippocampus","hippocampus"),
    ("thalamus","thalamus"),("caudate","caudate"),("putamen","putamen"),("pallidum","pallidum"),
    ("accumbens","accumbens"),("ventral_diencephalon_incl_hypothalamus","ventral_diencephalon_incl_hypothalamus"),
    ("cerebellum","cerebellum"),("brainstem","brainstem"),("corpus_callosum","corpus_callosum"),
    ("csf_and_ventricles","csf_and_ventricles")]:
    m, s = H[col].mean(), H[col].std(ddof=1)
    add("Homo sapiens (newborn)", "M-CRIB cohort mean, n=10", region, round(m,2), "cm^3",
        round(100*m/H["total_brain_tissue"].mean(),2), "% of total brain tissue volume",
        HUM_SRC, HUM_METH, "directly_measured_group_mean", "high",
        f"SD {s:.2f} cm^3 across 10 subjects; per-subject values in outputs/human_volumes_per_subject.csv")
add("Homo sapiens (newborn)", "M-CRIB cohort mean, n=10", "intracranial_labelled_total_incl_CSF",
    round(H["total_brain_tissue"].mean()+H["csf_and_ventricles"].mean(),2), "cm^3", None, "",
    HUM_SRC, HUM_METH, "directly_measured_group_mean", "high",
    "Tissue + all labelled CSF (incl. extra-axial); bracket for comparison with filled-mask volumes")

WU = "Wu et al. 2025, JAMA Pediatrics (doi:10.1001/jamapediatrics.2025.0277), n=96 term controls, mean PMA 42.84 wk"
for region, v in [("total_brain_volume",407.06),("cortical_volume",176.35),("white_matter_volume",166.65),
                  ("cerebellum",24.99),("brainstem",7.18),("amygdala_bilateral_sum",1.06)]:
    add("Homo sapiens (newborn)", "published cohort mean, n=96", region, v, "cm^3", None, "",
        WU, "published cohort volumetry (automated segmentation)", "literature", "high",
        "Independent cross-check of M-CRIB values; amygdala differs (1.06 vs 1.64) - segmentation-protocol difference, reported not averaged")

add("Panthera leo (adult)", "Brain Catalogue specimen, n=1, age/sex unstated", "total_brain_volume",
    LION_VOL, "cm^3", 100.0, "% of itself (reference)", "Brain Catalogue / Zenodo record 44855, ex vivo MRI 0.3 mm iso",
    "Otsu threshold mask, largest component, holes filled (this repo: scripts/volumetry_lion.py)",
    "directly_measured_single_specimen", "medium",
    f"Threshold sensitivity: {LION_LO}-{LION_HI} cm^3 for +/-10% threshold; mask includes internal CSF spaces (holes filled), excludes extra-axial space; fixation shrinkage expected vs in vivo")
SAKAI = "Sakai et al. 2016, Front. Neuroanat. 10:99 (PMC5071314), CT virtual endocasts, n=14 adults (8M/6F)"
for region, v, pct in [("endocranial_volume",244.42,100.0),("anterior_cerebrum",17.23,7.1),
                       ("posterior_cerebrum",170.06,69.6),("cerebellum_plus_brainstem",50.55,20.7)]:
    add("Panthera leo (adult)", "published cohort mean, n=14", region, v, "cm^3", pct,
        "% of endocranial volume", SAKAI, "CT endocast volumetry", "literature", "high",
        "Endocast includes meninges/CSF space - larger than brain tissue volume; regional boundaries are Sakai's planes, NOT homologous to DKT frontal cortex" if region=="anterior_cerebrum" else "Endocast measure - includes meninges/CSF space")
JM = "Jardim-Messeder et al. 2017, Front. Neuroanat. 11:118, n=1"
add("Panthera leo (adult)", "single specimen, n=1", "brain_mass", 198.9, "g", None, "", JM,
    "dissection + isotropic fractionator", "literature", "medium", "Body mass 180 kg")
add("Panthera leo (adult)", "single specimen, n=1", "cerebral_cortex_mass", 139.9, "g", 70.3,
    "% of brain mass", JM, "dissection + isotropic fractionator", "literature", "medium",
    "Mass fraction, not volume fraction - do not mix with cm^3 rows")
add("Panthera leo (adult)", "single specimen, n=1", "cortical_neuron_count", 545, "million neurons",
    None, "", JM, "isotropic fractionator", "literature", "medium", "Whole-brain neurons ~4.7 billion (same specimen)")

for region, why in [
    ("amygdala","No published lion amygdala volume exists; no validated felid subcortical segmentation model; manual delineation on a single ex vivo scan would be unvalidated - not fabricated"),
    ("hippocampus","Same as amygdala - no published value, no validated segmentation route for n=1 ex vivo lion"),
    ("hypothalamus","No published value; structure not separable with available tools/data"),
    ("periaqueductal_gray","No published value; below reliable delineation on this contrast/resolution without a felid atlas"),
    ("frontal_cortex","No DKT-homologous parcellation exists for lion; closest published region is Sakai's anterior cerebrum (different boundary definition) - listed separately, not equated"),
    ("white_matter_volume","Ex vivo T2/T1 contrast in this scan does not support validated GM/WM segmentation; no lion tissue-class volumes published"),
    ("diffusion_metrics_FA_MD","No openly available lion diffusion MRI exists (Oxford Digital Brain Bank has wolf dMRI, no felid)"),
    ("functional_connectivity","Post-mortem specimen - no functional data can exist for this scan; no in vivo lion rs-fMRI dataset is publicly available")]:
    add("Panthera leo (adult)", "n/a", region, None, "", None, "", "searched 2026-11-16 (see report)",
        "not measurable with available data", "unavailable", "n/a", why)
for region, why in [
    ("hypothalamus_standalone","Not a label in M-CRIB 2.0; hypothalamus is inside the VentralDC label, which IS measured above as ventral_diencephalon_incl_hypothalamus"),
    ("periaqueductal_gray","Not labelled in any open neonatal atlas found (M-CRIB, ALBERTs, Makropoulos)"),
    ("diffusion_metrics_FA_MD","Open newborn dMRI with segmentations does not exist; dHCP diffusion data are gated (NDA collection 3955). M-CRIB-WM provides DEC maps only, not regional FA/MD"),
    ("functional_connectivity","dHCP rs-fMRI gated (NDA); no open newborn rs-fMRI with parcellation was found")]:
    add("Homo sapiens (newborn)", "n/a", region, None, "", None, "", "searched 2026-11-16 (see report)",
        "not measurable with openly available data", "unavailable", "n/a", why)

df = pd.DataFrame(rows)
df.to_csv("outputs/measurements.csv", index=False)
print(f"{len(df)} rows written to outputs/measurements.csv")
print(df.groupby(['species','value_type']).size().to_string())
