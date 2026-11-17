"""Newborn white-matter volumetry from M-CRIB-WM combined parcellations.
WM tract labels are the >=30000 values in the largerange encoding; names from the
M-CRIB-WM itk label file. Per-subject volumes + group summary; total labelled WM
tract volume cross-checked against the M-CRIB 2.0 cerebral WM total (labels 2/41)."""
import nibabel as nib, numpy as np, pandas as pd, re, os

WM_DIR = "data/human_infant/mcrib_wm"
names = {}
for line in open(os.path.join(WM_DIR, "M-CRIB-2-0_and_M-CRIB-WM_labels_itk-format_largerange.txt")):
    m = re.match(r'\s*(\d+)\s+.*?"([^"]+)"', line)
    if m and int(m.group(1)) >= 30000: names[int(m.group(1))] = m.group(2)
print("WM regions:", len(names))

rows = []
for s in range(1, 11):
    p = os.path.join(WM_DIR, f"M-CRIB-WM_and_M-CRIB_2-0_P{s:02d}_parc_largerange.nii.gz")
    im = nib.load(p); a = np.asanyarray(im.dataobj)
    vox = float(np.prod(im.header.get_zooms())) / 1000.0
    row = {"subject": f"P{s:02d}"}
    tot = 0.0
    for lab, nm in sorted(names.items()):
        v = float((a == lab).sum()) * vox; row[nm] = round(v, 3); tot += v
    row["wm_tracts_total_cm3"] = round(tot, 2)
    rows.append(row)
df = pd.DataFrame(rows)
df.to_csv("outputs/human_wm_volumes_per_subject.csv", index=False)
g = df.drop(columns=["subject"])
summ = pd.DataFrame({"mean_cm3": g.mean().round(2), "sd_cm3": g.std().round(2)}).sort_values("mean_cm3", ascending=False)
print(summ.head(20).to_string())
print("\nWM tracts total: mean %.2f +- %.2f cm3 (M-CRIB 2.0 cerebral WM total was 161.06 +- 14.08 — tracts are a subset of all WM, so lower is expected)" %
      (df["wm_tracts_total_cm3"].mean(), df["wm_tracts_total_cm3"].std()))
cc = [c for c in df.columns if c.startswith("cc_")]
print("Corpus callosum segments sum: mean %.2f cm3 (2.0 CC label was 0.76)" % df[cc].sum(axis=1).mean())
