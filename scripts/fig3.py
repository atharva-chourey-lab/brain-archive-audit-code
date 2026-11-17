"""Figure 3 from the saved morphospace features (plot-only; data from scripts/morphospace.py)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
df = pd.read_csv("outputs/morphospace_features.csv")
FEATS = ["log10_vol", "gyrification_proxy", "elong_long", "elong_flat"]
Z = (df[FEATS] - df[FEATS].mean()) / df[FEATS].std(ddof=1)
S = np.linalg.svd(Z.values, full_matrices=False, compute_uv=False)
var = S ** 2 / (S ** 2).sum()
fig, ax = plt.subplots(figsize=(9, 7))
sp = df[df.group == "brain_catalogue"]
ax.scatter(sp.PC1, sp.PC2, s=70, color="#d88a3b", zorder=3)
for _, r in sp.iterrows():
    ax.annotate(r.point, (r.PC1, r.PC2), fontsize=8, xytext=(4, 4), textcoords="offset points")
inf = df[df.group == "human_infant_mcrib"]
ax.scatter(inf.PC1, inf.PC2, s=45, color="#3b7dd8", zorder=3, label="Human newborns (n=10, M-CRIB)")
ax.scatter([inf.PC1.mean()], [inf.PC2.mean()], s=240, marker="*", color="#3b7dd8", zorder=4)
for _, r in df[df.group.isin(["template", "proxy_template"])].iterrows():
    ax.scatter([r.PC1], [r.PC2], s=90, marker="D", color="#666666", zorder=3)
    ax.annotate(r.point, (r.PC1, r.PC2), fontsize=8, xytext=(4, 4), textcoords="offset points")
li = df[df.point == "lion"].iloc[0]
ax.scatter([li.PC1], [li.PC2], s=280, marker="*", color="#d88a3b", zorder=5)
ax.set_xlabel(f"PC1 ({var[0]*100:.0f}% of variance) - size + elongation")
ax.set_ylabel(f"PC2 ({var[1]*100:.0f}% of variance) - folding (inverted)")
ax.set_title("Figure 3 - A structural morphometric space (Chen-style geometry, structural edition).\n"
             "Same four mask features for every brain; stars = lion and newborn centroid; diamonds = templates.\n"
             "Orangutan and red squirrel excluded on QC (see report). Descriptive embedding, n=1 per species.", fontsize=9)
ax.legend(fontsize=8); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("outputs/fig3_morphospace.png", dpi=200)
print("fig3 saved; variance:", np.round(var, 3))
