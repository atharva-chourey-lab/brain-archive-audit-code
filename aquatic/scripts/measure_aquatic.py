"""AQUATIC THREAD — Phase 2 measurement.

Replicates the project's established pipeline EXACTLY on the aquatic /
semi-aquatic species of the Brain Catalogue download:
  - Brain volume: Otsu mask of the species MRI, copied verbatim from
    scripts/cross_species_table.py (v1): Otsu threshold on nonzero voxels,
    fill holes, largest connected component.
  - Label volumes: v2 rules (scripts/cross_species_table_v2.py): each label
    file's OWN header zooms; a label counts as real only if nz > 1000.
Forensic extras (this thread): per-label component structure, centroid
laterality for the hippocampus files, label-vs-mask containment (what share
of a label's voxels fall inside the Otsu brain mask), the Bottlenose
multi-structure grid check (its Cerebellum/Corpus_callosum files carry
different zooms from its MRI), and a QC contact sheet.

Outputs: aquatic/measurements_aquatic_raw.json, aquatic/qc_aquatic_sheet.png
Run from the project root:  .venv/bin/python aquatic/scripts/measure_aquatic.py
"""
import nibabel as nib, numpy as np, os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

ROOT = "data/brain_catalogue_full"
OUT = "aquatic"
SPECIES = ["Bottlenose_dolphin", "La_Plata_dolphin", "Platypus",
           "Nile_crocodile", "Nursehound"]
inv = json.load(open("outputs/braincatalogue_inventory.json"))


def otsu_mask(d):
    """Verbatim from scripts/cross_species_table.py."""
    nz = d[d > 0]
    if len(nz) == 0:
        return None
    hist, edges = np.histogram(nz, bins=256)
    w = hist / hist.sum(); om = np.cumsum(w); mu = np.cumsum(w * np.arange(256))
    s2 = (mu[-1] * om - mu) ** 2 / (om * (1 - om) + 1e-12)
    thr = float(edges[int(np.nanargmax(s2))])
    m = ndimage.binary_fill_holes(d > thr)
    lab, n = ndimage.label(m)
    if n == 0:
        return m
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)


REPAIRS = {}


def load(p):
    """Load a NIfTI; if nibabel refuses it, attempt the one documented repair
    this dataset needs and record it in REPAIRS (never writes to disk):
    Nile_crocodile/MRI.nii.gz has a zeroed magic string and datatype field,
    but sizeof_hdr=348, valid dims/pixdim, vox_offset=352, and a payload
    whose byte count exactly equals the voxel count -> uint8 data."""
    try:
        im = nib.load(p)
        a = np.squeeze(np.asanyarray(im.dataobj))
        if a.ndim == 4:
            a = a[..., 0]
        return a, np.array(im.header.get_zooms()[:3], float), im.shape
    except Exception:
        import gzip, struct
        raw = gzip.open(p, "rb").read()
        assert struct.unpack("<i", raw[0:4])[0] == 348, "not a NIfTI-1 header"
        dims = struct.unpack("<8h", raw[40:56])
        shape = tuple(int(x) for x in dims[1:4])
        nvox = int(np.prod(shape))
        off = int(struct.unpack("<f", raw[108:112])[0])
        assert len(raw) - off == nvox, "payload is not 1 byte/voxel"
        a = np.frombuffer(raw[off:off + nvox], dtype=np.uint8) \
              .reshape(shape, order="F")
        zooms = np.array(struct.unpack("<8f", raw[76:108])[1:4], float)
        REPAIRS[p] = ("header repair (in-memory only): magic/datatype fields "
                      "are zeroed in the file; payload byte count proves "
                      "uint8; dims/pixdim read from the surviving header")
        print(f"  !! repaired header in memory for {p}")
        return a, zooms, shape


def components(mask):
    lab, n = ndimage.label(mask)
    if n == 0:
        return {"n_components": 0, "sizes_vox": []}
    sizes_arr = ndimage.sum(mask, lab, range(1, n + 1)).astype(int)
    cents = ndimage.center_of_mass(mask, lab, range(1, n + 1))
    order = np.argsort(sizes_arr)[::-1]
    sizes = sorted((int(s) for s in sizes_arr), reverse=True)
    return {"n_components": n,
            "sizes_vox": sizes[:6],
            "largest_share": round(sizes[0] / sum(sizes), 4),
            "centroids_top3": [[round(float(c), 1) for c in cents[i]]
                               for i in order[:3]]}


results = {}
fig, axes = plt.subplots(2, 3, figsize=(17, 11))
axes = axes.flat
for i, species in enumerate(SPECIES):
    sdir = os.path.join(ROOT, species)
    v = inv[species]
    rec = {"files": {}}
    d, mzooms, mshape = load(os.path.join(sdir, v["brain"]))
    d = d.astype(np.float32)
    vox_cm3_mri = float(np.prod(mzooms)) / 1000.0
    mask = otsu_mask(d)
    brain_vox = int(mask.sum())
    rec["mri"] = {"file": v["brain"], "shape": list(mshape),
                  "zooms_mm": [round(float(z), 4) for z in mzooms],
                  "otsu_brain_vox": brain_vox,
                  "otsu_brain_cm3": round(brain_vox * vox_cm3_mri, 2)}
    print(f"\n===== {species}: MRI {v['brain']} zooms={mzooms} "
          f"Otsu brain = {rec['mri']['otsu_brain_cm3']} cm3 ({brain_vox} vox)")
    ax = axes[i]
    zz = d.shape[2] // 2
    ax.imshow(np.rot90(d[:, :, zz]), cmap="gray")
    ax.contour(np.rot90(mask[:, :, zz].astype(float)), levels=[0.5],
               colors="cyan", linewidths=0.6)
    for lf in v.get("atlas", []):
        p = os.path.join(sdir, lf)
        key = lf[:-7]
        a, z, shp = load(p)
        nz = int((a > 0).sum())
        own_cm3 = round(nz * float(np.prod(z)) / 1000.0, 3)
        info = {"file": lf, "shape": list(shp),
                "zooms_mm": [round(float(x), 4) for x in z],
                "nz": nz, "vol_cm3_own_zooms": own_cm3,
                "vol_cm3_at_mri_zooms": round(nz * vox_cm3_mri, 3),
                "unique_values": [float(x) for x in np.unique(a)][:8],
                "value_counts": {str(float(x)): int((a == x).sum())
                                 for x in np.unique(a) if x > 0}}
        if nz > 0:
            info.update(components(a > 0))
            if a.shape == mask.shape:
                info["frac_vox_inside_otsu_mask"] = round(
                    float(((a > 0) & mask).sum()) / nz, 4)
            # overlay the largest label on its best slice
            if key.lower() in ("telencephalon", "atlas", "hippocampus",
                               "cerebellum"):
                zbest = int(np.argmax([(a[:, :, k] > 0).sum()
                                        for k in range(a.shape[2])]))
                ax.imshow(np.rot90(d[:, :, zbest]), cmap="gray")
                ax.contour(np.rot90(mask[:, :, zbest].astype(float)),
                           levels=[0.5], colors="cyan", linewidths=0.6)
                ax.imshow(np.ma.masked_where(
                    np.rot90(a[:, :, zbest]) == 0,
                    np.rot90(a[:, :, zbest].astype(float))),
                    cmap="Reds", alpha=0.75, interpolation="nearest")
        rec["files"][key] = info
        print(f"  {key:16s} nz={nz:>9} own-zooms={own_cm3:>9} cm3 "
              f"mri-zooms={info['vol_cm3_at_mri_zooms']:>9} cm3 "
              f"comps={info.get('n_components')} "
              f"inside_mask={info.get('frac_vox_inside_otsu_mask')}")
    ax.set_title(species, fontsize=10); ax.axis("off")
    results[species] = rec
axes[len(SPECIES)].axis("off")
fig.suptitle("Aquatic QC — Otsu brain mask (cyan) + principal label (red)",
             fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.98])
fig.savefig(os.path.join(OUT, "qc_aquatic_sheet.png"), dpi=110)
results["_header_repairs"] = REPAIRS
with open(os.path.join(OUT, "measurements_aquatic_raw.json"), "w") as f:
    json.dump(results, f, indent=1)
print("\nwrote aquatic/measurements_aquatic_raw.json + qc_aquatic_sheet.png")
