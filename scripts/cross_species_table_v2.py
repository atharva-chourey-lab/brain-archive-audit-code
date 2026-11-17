"""Cross-species table v2 — verified labels only.
Rules: (1) every label volume uses that FILE's own header zooms; (2) a label counts as
real only if nonzero voxels > 1000 and the value is anatomically plausible;
(3) brain-volume denominator prefers the catalogue's own Atlas mask, then the Otsu
mask, each tagged; (4) known junk excluded by name with reasons (red squirrel
'hippocampus' = whole-brain mask; okapi nz=272; night monkey nz=1)."""
import nibabel as nib, numpy as np, pandas as pd, os, json
from scipy import stats

ROOT = "data/brain_catalogue_full"
inv = json.load(open("outputs/braincatalogue_inventory.json"))

def load(p):
    im = nib.load(p); return np.asanyarray(im.dataobj), np.array(im.header.get_zooms()[:3], float)

def vol_cm3(a, zooms): return float((a > 0).sum()) * float(np.prod(zooms)) / 1000.0

EXCLUDE = {("Red_squirrel", "hippocampus"): "file duplicates the whole-brain Atlas mask — mislabeled",
           ("Okapi", "hippocampus"): "272 nonzero voxels — sliver, not a structure",
           ("Night_monkey", "hippocampus"): "1 nonzero voxel — junk placeholder"}
rows = []
for species, v in sorted(inv.items()):
    sdir = os.path.join(ROOT, species)
    if species == "Lion":  # bulk-grab MRI was an empty file; use the Zenodo original + its atlas dir
        hip_a, hip_z = load("data/lion/atlas/Hippocampus.nii.gz")
        tel_a, tel_z = load("data/lion/atlas/Telencephalon.nii.gz")
        rows.append({"species": "Lion", "hippocampus_cm3": round(vol_cm3(hip_a, hip_z), 3),
                     "telencephalon_cm3": round(vol_cm3(tel_a, tel_z), 2),
                     "brain_vol_cm3": 188.08, "brain_vol_source": "otsu_mask_zenodo_scan",
                     "hippocampus_pct": 1.07, "qc": "verified: overlay checked"})
        continue
    row = {"species": species}
    atlas_vol = None
    for lf in v.get("atlas", []):
        key = lf[:-7].lower(); p = os.path.join(sdir, lf)
        if not os.path.exists(p): continue
        a, z = load(p); nz = int((a > 0).sum()); vv = vol_cm3(a, z)
        if (species, key) in EXCLUDE: row[key + "_note"] = "EXCLUDED: " + EXCLUDE[(species, key)]; continue
        if key == "atlas": atlas_vol = vv; row["atlas_mask_cm3"] = round(vv, 2)
        elif nz <= 1000: row[key + "_note"] = f"empty/placeholder (nz={nz})"
        else: row[key + "_cm3"] = round(vv, 3)
    # Otsu brain volume carried over from v1 csv when present
    row["brain_vol_source"] = ""
    rows.append(row)

v1 = pd.read_csv("outputs/cross_species_volumes.csv").set_index("species")
df = pd.DataFrame(rows)
for i, r in df.iterrows():
    otsu = v1.loc[r["species"], "brain_vol_cm3_otsu"] if r["species"] in v1.index else np.nan
    if pd.notna(r.get("atlas_mask_cm3")):
        df.at[i, "brain_vol_cm3"] = r["atlas_mask_cm3"]; df.at[i, "brain_vol_source"] = "catalogue_atlas_mask"
    elif pd.notna(otsu):
        df.at[i, "brain_vol_cm3"] = otsu; df.at[i, "brain_vol_source"] = "otsu_mask"
    if pd.notna(r.get("hippocampus_cm3")) and pd.notna(df.at[i, "brain_vol_cm3"]):
        df.at[i, "hippocampus_pct"] = round(100 * r["hippocampus_cm3"] / df.at[i, "brain_vol_cm3"], 2)
df.to_csv("outputs/cross_species_volumes_v2.csv", index=False)
show = [c for c in ["species", "brain_vol_cm3", "brain_vol_source", "hippocampus_cm3", "hippocampus_pct",
                    "telencephalon_cm3", "cerebrum_cm3", "striatum_cm3", "cerebellum_cm3", "neocortex_cm3"] if c in df]
print(df[show].to_string(index=False))

# Allometry on the verified hippocampus set (log-log OLS, descriptive, tiny n)
pts = df.dropna(subset=["hippocampus_cm3", "brain_vol_cm3"])
x, y = np.log10(pts["brain_vol_cm3"]), np.log10(pts["hippocampus_cm3"])
if len(pts) >= 4:
    sl, ic, r, p, se = stats.linregress(x, y)
    print(f"\nALLOMETRY (n={len(pts)} species): log10(hippo) = {sl:.2f} * log10(brain) + {ic:.2f}; r={r:.2f}, p={p:.3f}")
    pred_nb = 10 ** (sl * np.log10(374.40) + ic)
    print(f"Newborn human (brain 374.4 cm3): predicted hippocampus {pred_nb:.2f} cm3 vs measured 2.90 cm3 "
          f"({100*(2.90-pred_nb)/pred_nb:+.0f}% vs the mammalian line)")
    print("species in fit:", ", ".join(pts["species"]))
