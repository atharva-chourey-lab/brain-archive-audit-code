"""Render coronal tracing batches for the bottlenose hippocampus delineation (Item 1).
Usage: .venv/bin/python scripts/render_trace_batch.py 104 108 112 ...
Writes outputs/dolphin_feasibility/trace_<first>_<last>.png, 2 slices per figure,
panels = the two horn-wall crops (ax0 112-205 and 243-336), ax2 58-126, grid-labelled.
"""
import sys
import nibabel as nib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

base = 'data/brain_catalogue_full/Bottlenose_dolphin/'
mri = nib.load(base + 'MRI-n4.nii.gz').get_fdata()
slices = [int(x) for x in sys.argv[1:]]
for si in range(0, len(slices), 2):
    ys = slices[si:si + 2]
    fig, axes = plt.subplots(2, 2, figsize=(20, 11))
    for r, y in enumerate(ys):
        for c, (x0, x1) in enumerate([(112, 205), (243, 336)]):
            ax = axes[r, c]
            img = mri[x0:x1, y, 58:126].T[::-1, :]
            ax.imshow(img, cmap='gray', vmin=0, vmax=240, interpolation='nearest')
            ax.set_xticks(range(0, x1 - x0, 10))
            ax.set_xticklabels(range(x0, x1, 10), fontsize=7)
            ax.set_yticks(range(0, 68, 5))
            ax.set_yticklabels([125 - t for t in range(0, 68, 5)], fontsize=7)
            ax.grid(color='cyan', linewidth=0.3, alpha=0.35)
            ax.set_title(f'ax1={y} ax0 {x0}-{x1} (x=ax0, y=ax2)', fontsize=10)
    plt.tight_layout()
    plt.savefig(f'outputs/dolphin_feasibility/trace_{ys[0]}_{ys[-1]}.png', dpi=110)
    plt.close(fig)
    print('saved', ys)
