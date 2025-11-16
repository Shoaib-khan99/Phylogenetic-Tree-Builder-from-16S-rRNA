#!/usr/bin/env python
import os
import subprocess

ALN = "../results/aligned.fasta"
OUTDIR = "../results/ml_tree"

os.makedirs(OUTDIR, exist_ok=True)

cmd = [
    "iqtree", "-s", ALN,
    "-m", "GTR+F+R4",  # Best model via ModelFinder
    "-bb", "1000",     # Ultrafast bootstrap
    "-nt", "AUTO",
    "-pre", f"{OUTDIR}/silva_ml"
]

print("Running IQ-TREE...")
subprocess.run(cmd, check=True)
print(f"ML tree saved to {OUTDIR}/silva_ml.treefile")
