#!/bin/bash
set -euo pipefail

CONFIG="../config.yaml"
RELEASE=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG'))['silva_release'])")
SAMPLE_SIZE=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG'))['sample_size'])")
SEED=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG'))['seed'])")

mkdir -p raw fasta

echo "Downloading SILVA ${RELEASE} SSU Ref NR 99..."
wget -O raw/SILVA_${RELEASE}_SSURef_NR99.fasta.gz \
  https://www.arb-silva.de/fileadmin/silva_databases/release_${RELEASE//./}/Exports/SILVA_${RELEASE}_SSURef_NR99_tax_silva.fasta.gz

echo "Extracting and filtering..."
gunzip -c raw/SILVA_${RELEASE}_SSURef_NR99.fasta.gz | \
  awk 'BEGIN{RS=">"; FS="\n"} 
       NR>1 {
         id=$1; seq=$2; 
         gsub(/U|T/, "T", seq); 
         len=length(seq); 
         if(len>=1200 && len<=1600) print ">"id"\n"seq
       }' > raw/filtered.fasta

echo "Sampling $SAMPLE_SIZE sequences..."
shuf -n $SAMPLE_SIZE --random-source=<(openssl enc -aes-256-ctr -pass pass:"$SEED" -nosalt </dev/zero 2>/dev/null) \
  raw/filtered.fasta > fasta/silva_sample.fasta

echo "Done! Saved to fasta/silva_sample.fasta"
