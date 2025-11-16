#!/bin/bash
set -euo pipefail

INPUT="../data/fasta/silva_sample.fasta"
OUTPUT="../results/aligned.fasta"

mafft --auto --thread 8 "$INPUT" > "$OUTPUT"
echo "Alignment saved to $OUTPUT"
