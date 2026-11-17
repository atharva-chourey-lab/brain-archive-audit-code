"""Figure 1: matched anatomical sections (infant T2 + parcellation overlay; lion MRI + mask).
Figure 2: absolute volumes and normalised proportions with explicit denominators."""
import nibabel as nib, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

H = pd.read_csv("outputs/human_volumes_per_subject.csv")
sid = H.iloc[(H.total_brain_tissue - H.total_brain_tissue.median()).abs().argmin()].subject
t2 = nib.load(f"data/human_infant/mcrib2/subjects/M-CRIB_{sid}_T2.nii.gz")
parc = nib.load(f"data/human_infant/mcrib2/subjects/M-CRIB_2-0_{sid}_parc.nii.gz")
t2d = t2.get_fdata(dtype=np.float32); pd_ = np.asanyarray(parc.dataobj)
tz = float(t2.header.get_zooms()[0])
lion = nib.load("data/lion/MRI-n4.nii.gz"); ld = lion.get_fdata(dtype=np.float32)
lmask = np.load("outputs/lion_brainmask_otsu.npy"); lz = 0.3

def com(mask): return np.array(np.where(mask)).mean(axis=1).astype(int)

def bbox_of(ref, pad=6):
    ys, xs = np.where(ref > 0)
    return (slice(max(0, ys.min()-pad), ys.max()+pad), slice(max(0, xs.min()-pad), xs.max()+pad))

def panel(ax, base, overlay, vox, title, mode):
    b0 = np.rot90(base); o0 = np.rot90(overlay)
    bb = bbox_of(b0 if mode == "parc" else o0)
    b, o = b0[bb], o0[bb]
    if mode == "parc":
        ax.imshow(b, cmap="gray", vmin=np.percentile(t2d[t2d > 0], 2), vmax=np.percentile(t2d[t2d > 0], 98))
        ax.imshow(np.ma.masked_where(o == 0, o), cmap="nipy_spectral", alpha=0.45, interpolation="nearest")
    else:
        ax.imshow(b, cmap="gray", vmin=5, vmax=235)
        ax.contour(o, levels=[0.5], colors="red", linewidths=0.8)
    ax.set_title(title, fontsize=9); ax.axis("off")
    n = 20 / vox
    ax.plot([8, 8 + n], [b.shape[0] - 10, b.shape[0] - 10], color="white", lw=3, solid_capstyle="butt")
    ax.text(8, b.shape[0] - 13, "20 mm", color="white", fontsize=7, va="bottom")

fig, axes = plt.subplots(2, 3, figsize=(11, 7.5))
c = com(pd_ > 0)
for ax, sl, ttl in zip(axes[0], [np.s_[c[0], :, :], np.s_[:, c[1], :], np.s_[:, :, c[2]]], ["Sagittal", "Coronal", "Axial"]):
    panel(ax, t2d[sl], pd_[sl], tz, f"Human newborn ({sid}) — {ttl}", "parc")
lc = com(lmask)
for ax, sl, ttl in zip(axes[1], [np.s_[lc[0], :, :], np.s_[:, lc[1], :], np.s_[:, :, lc[2]]], ["Sagittal", "Coronal", "Axial"]):
    panel(ax, ld[sl], lmask[sl], lz, f"Adult lion (ex vivo) — {ttl}", "mask")
fig.suptitle("Figure 1 — Matched anatomical sections at each brain's centre of mass.\n"
             "Top: newborn T2 with 94-region manual parcellation overlay (M-CRIB 2.0). Bottom: lion structural MRI, red contour = Otsu brain mask used for volumetry.\n"
             "Matched by plane only — no cross-species voxel correspondence is implied.", fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.92]); fig.savefig("outputs/fig1_matched_sections.png", dpi=200)
print("fig1 done, infant subject:", sid)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.8))
names = ["Newborn tissue\n(n=10)", "Newborn tissue+CSF\n(n=10)", "Lion MRI mask\n(n=1)", "Lion endocranial\nCT (n=14)"]
vals = [374.4, 474.0, 188.1, 244.4]
cols = ["#3b7dd8", "#9dbfe8", "#d88a3b", "#e8c39d"]
bars = a1.bar(names, vals, color=cols)
a1.errorbar([0, 1], [374.4, 474.0], yerr=[37.0, 43.5], fmt="none", ecolor="k", capsize=4)
a1.plot([2, 2], [178.2, 193.4], color="k", lw=2)
a1.set_ylabel("Volume (cm³)")
a1.set_title("Absolute volumes (bars: SD across subjects;\nlion whisker = ±10% threshold band)", fontsize=9)
for b, v in zip(bars, vals): a1.text(b.get_x() + b.get_width() / 2, v + 10, f"{v:.0f}", ha="center", fontsize=9)
labels = ["Cerebellum +\nbrainstem", "Frontal (DKT) /\nanterior cerebrum*", "Cortical gray /\ncortex mass*"]
inf = [7.7, 13.9, 43.0]; lio = [20.7, 7.1, 70.3]
y = np.arange(len(labels)); h = 0.36
a2.barh(y + h / 2, inf, h, color="#3b7dd8", label="Newborn (% of tissue volume)")
a2.barh(y - h / 2, lio, h, color="#d88a3b", label="Lion (% of endocranial vol / *brain mass)")
a2.set_yticks(y); a2.set_yticklabels(labels, fontsize=8); a2.invert_yaxis()
a2.set_xlabel("% of reference volume — denominators differ, see caption")
a2.set_title("Normalised proportions", fontsize=9)
a2.legend(fontsize=7.5, loc="upper right")
fig.suptitle("Figure 2 — Absolute and normalised comparison. *Frontal and cortex rows pair non-identical definitions\n"
             "(DKT frontal parcels vs Sakai's anterior-cerebrum plane; cortical GM volume share vs cortical mass share) — closest available, not homologues.", fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.9]); fig.savefig("outputs/fig2_delta.png", dpi=200)
print("fig2 done")
