#!/bin/bash
set -euo pipefail

echo "Step 1: Download SILVA 16S"
bash data/download_silva.sh

echo "Step 2: Align with MAFFT"
bash align/run_mafft.sh

echo "Step 3: Build NJ Tree"
python tree/build_nj.py

echo "Step 4: Build ML Tree"
python tree/build_ml.py

echo "Step 5: Visualize with Plotly"
python visualize/plot_tree.py

echo "Done! Check results/ folder"
