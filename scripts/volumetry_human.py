"""M-CRIB 2.0 regional volumetry: per-subject volumes from the 94-region manual
parcellations, grouped into the comparison regions. Writes per-subject CSV."""
import nibabel as nib, numpy as np, pandas as pd, glob, re

LAB = {}
for line in open("data/human_infant/mcrib2/labels/M-CRIB_2-0_labels_itk_format.txt"):
    parts = line.strip().split('"')
    if len(parts) >= 2:
        LAB[parts[1]] = int(parts[0].split()[0])
def ids(names): return [LAB[n] for n in names]
def hemi(base): return ids([f"Left-{base}", f"Right-{base}"])

CTX = [v for k, v in LAB.items() if k.startswith("ctx-")]
FRONTAL_NAMES = ["caudalmiddlefrontal","lateralorbitofrontal","medialorbitofrontal",
    "parsopercularis","parsorbitalis","parstriangularis","precentral",
    "rostralmiddlefrontal","superiorfrontal","frontalpole"]
FRONTAL = [LAB[f"ctx-{h}-{n}"] for h in ("lh","rh") for n in FRONTAL_NAMES]
CSF_IDS = ids(["CSF"]) + hemi("Lateral-Ventricle") + ids(["3rd-Ventricle","4th-Ventricle"])

GROUPS = {
  "cortical_gray_matter": CTX,
  "cerebral_white_matter": hemi("Cerebral-White-Matter"),
  "frontal_cortex_dkt": FRONTAL,
  "amygdala": hemi("Amygdala"),
  "hippocampus": hemi("Hippocampus"),
  "thalamus": hemi("Thalamus"),
  "caudate": hemi("Caudate"),
  "putamen": hemi("Putamen"),
  "pallidum": hemi("Pallidum"),
  "accumbens": hemi("Accumbens-area"),
  "ventral_diencephalon_incl_hypothalamus": hemi("VentralDC"),
  "cerebellum": ids(["Cerebellar_vermis_superior_posterior","Cerebellar_vermis_anterior",
                     "Cerebellar_vermis_inferior_posterior","LH_Cerebellar_hemisphere",
                     "RH_Cerebellar_hemisphere"]),
  "brainstem": ids(["brainstem"]),
  "corpus_callosum": ids(["Corpus_Callosum"]),
  "csf_and_ventricles": CSF_IDS,
}
rows = []
for f in sorted(glob.glob("data/human_infant/mcrib2/subjects/*_parc.nii.gz")):
    subj = re.search(r"(P\d+)", f).group(1)
    img = nib.load(f); d = np.asanyarray(img.dataobj).astype(int)
    vv = float(np.prod(img.header.get_zooms())) / 1000.0  # cm^3 per voxel
    rec = {"subject": subj}
    tissue = np.isin(d, [v for k, v in LAB.items() if v != 0 and v not in CSF_IDS])
    rec["total_brain_tissue"] = float(tissue.sum() * vv)
    for g, gids in GROUPS.items():
        rec[g] = float(np.isin(d, gids).sum() * vv)
    rows.append(rec)
df = pd.DataFrame(rows)
df.to_csv("outputs/human_volumes_per_subject.csv", index=False)
s = df.drop(columns="subject")
print("M-CRIB 2.0 group volumetry (cm^3), n =", len(df))
print(pd.DataFrame({"mean": s.mean(), "sd": s.std(ddof=1)}).round(2).to_string())
