"""TABLE V3 — v2 + the four atlas-propagated hippocampi, classes kept separate.

The 10 catalogue-label measurements remain the ONLY headline fit set. The four
propagated points (human via Harvard-Oxford; chimp/gorilla/wolf via D99) are
model estimates from a different method and are NEVER pooled into the headline
fit — they are reported with their deviations from the headline line, and a
second, sensitivity fit shows what including them would do to the line.
Brain-volume denominators are v2's, unchanged, for consistency."""
import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv("outputs/cross_species_volumes_v2.csv")

PROP = {
    # species: (hippocampus_cm3, note)
    "Human":       (6.85, "Harvard-Oxford atlas propagation (affine, model-estimated); QC overlay pass"),
    "Chimpanzee":  (1.48, "D99 macaque-atlas propagation (affine, model-estimated); overlay sparse/lopsided - PROVISIONAL, low confidence"),
    "Gorilla":     (1.76, "D99 macaque-atlas propagation (affine, model-estimated); overlay sparse - flagged"),
    "Gray_wolf":   (0.69, "D99 macaque-atlas propagation, CROSS-ORDER (affine, model-estimated); overlay pass (bilateral, in-territory)"),
}
df["data_class"] = np.where(df["hippocampus_cm3"].notna(), "catalogue_label", "none")
for sp, (vol, note) in PROP.items():
    i = df.index[df["species"] == sp]
    assert len(i) == 1, sp
    df.loc[i, "hippocampus_cm3"] = vol
    df.loc[i, "hippocampus_note"] = note
    df.loc[i, "data_class"] = "model_estimated_propagation"
df["hippocampus_pct"] = np.where(
    df["hippocampus_cm3"].notna() & df["brain_vol_cm3"].notna(),
    100.0 * df["hippocampus_cm3"] / df["brain_vol_cm3"], df["hippocampus_pct"])

def fit(sub):
    x = np.log10(sub["brain_vol_cm3"].astype(float))
    y = np.log10(sub["hippocampus_cm3"].astype(float))
    return stats.linregress(x, y)

lab = df[df["data_class"] == "catalogue_label"]
allm = df[df["hippocampus_cm3"].notna()]
f_lab, f_all = fit(lab), fit(allm)
print(f"HEADLINE fit (catalogue labels only, n={len(lab)}): slope {f_lab.slope:.3f}, "
      f"intercept {f_lab.intercept:.3f}, r {f_lab.rvalue:.3f}, p {f_lab.pvalue:.2g}")
print(f"SENSITIVITY fit (labels + propagated, n={len(allm)}): slope {f_all.slope:.3f}, "
      f"intercept {f_all.intercept:.3f}, r {f_all.rvalue:.3f}, p {f_all.pvalue:.2g}")

def predict(f, brain):
    return float(10 ** (f.intercept + f.slope * np.log10(brain)))

df["predicted_hippocampus_cm3"] = np.where(
    df["hippocampus_cm3"].notna() & df["brain_vol_cm3"].notna(),
    [predict(f_lab, b) if ok else np.nan for b, ok in
     zip(df["brain_vol_cm3"], df["hippocampus_cm3"].notna() & df["brain_vol_cm3"].notna())], np.nan)
df["deviation_pct"] = 100.0 * (df["hippocampus_cm3"] - df["predicted_hippocampus_cm3"]) / df["predicted_hippocampus_cm3"]

show = df[df["hippocampus_cm3"].notna()].sort_values("brain_vol_cm3")
print("\n species                brain    hipp  class                       predicted  deviation")
for _, r in show.iterrows():
    print(f" {r['species']:<22} {r['brain_vol_cm3']:7.2f} {r['hippocampus_cm3']:6.3f}  "
          f"{r['data_class']:<26} {r['predicted_hippocampus_cm3']:7.3f}  {r['deviation_pct']:+6.1f}%")

nb_pred = predict(f_lab, 374.40)
print(f"\nNewborn check (headline line): predicted {nb_pred:.2f} cm3 at 374.40 cm3 brain "
      f"vs measured 2.90 -> {100.0*(2.90-nb_pred)/nb_pred:+.1f}%")

df.to_csv("outputs/cross_species_volumes_v3.csv", index=False)
print("\nwrote outputs/cross_species_volumes_v3.csv")
