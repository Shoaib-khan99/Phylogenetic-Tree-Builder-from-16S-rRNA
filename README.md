# 16S rRNA Phylogenetic Tree Builder 🧬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Conda](https://img.shields.io/badge/conda-managed-green.svg)](https://docs.conda.io/)

Build **Neighbor-Joining** and **Maximum Likelihood** phylogenetic trees from **SILVA 16S rRNA** sequences using **MAFFT**, **BioPython**, **IQ-TREE**, and **interactive Plotly visualization**.

---

## Features
- Auto-download from **SILVA SSU Ref NR 99**
- Filter by sequence length
- **MAFFT** alignment
- **NJ** tree via BioPython
- **ML** tree via IQ-TREE (GTR+F+R4 + 1000 UFBoot)
- **Interactive HTML trees** with taxonomy coloring
- Static PNG export

---

## Quick Start

```bash
git clone https://github.com/yourname/16s-phylogeny-builder.git
cd 16s-phylogeny-builder
conda env create -f environment.yml
conda activate 16s-phylo
./run_all.sh

sample_size: 50
min_length: 900
max_length: 1800

cp my_16s.fasta data/fasta/silva_sample.fasta
