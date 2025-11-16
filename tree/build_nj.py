#!/usr/bin/env python
import os
from Bio import Phylo, AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import plotly.graph_objects as go
import plotly.io as pio

# Paths
ALN = "../results/aligned.fasta"
TREE_NJ = "../results/tree_nj.newick"

# Read alignment
align = AlignIO.read(ALN, "fasta")
print(f"Loaded {len(align)} sequences, length: {align.get_alignment_length()}")

# Calculate distance matrix (Kimura 2-parameter)
calculator = DistanceCalculator('identity')  # or 'blastn', 'trans'
dm = calculator.get_distance(align)

# Build NJ tree
constructor = DistanceTreeConstructor()
tree = constructor.nj(dm)

# Save
Phylo.write(tree, TREE_NJ, "newick")
print(f"NJ tree saved to {TREE_NJ}")
