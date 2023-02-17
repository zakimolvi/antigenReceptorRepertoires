#!/bin/bash
# Demultiplex reads by fastq splitting based off 3' index primers:
# 1. Demultiplex paired-end 2x250bp Illumina reads with index sequences on 3' end for 16 indices using MiGEC
# 2. Run MiXCR to align final TCR sequences

source /opt/anaconda3/etc/profile.d/conda.sh # required to be able to activate conda env in subshell

conda create -n r-environment r-essentials r-base
conda activate r-environment
pip install brew
brew install java

conda activate r-environment

# make sure you have ~/migec*/migec*.jar
# demultiplex paired-end input fastq.gz
java -jar ~/migec*/migec*.jar Checkout -cut --overlap --rc-barcodes barcode_migec.txt input_R1_001.fastq.gz output_R2_001.fastq.gz ./output_demultiplexed

# Run mixcr on paired reads from Amplicon-EZ seq of nested TCR products

run_mixcr () {
    mixcr analyze amplicon -s hsa --starting-material rna --5-end v-primers --3-end c-primers --adapters adapters-present --receptor-type tcr --contig-assembly --align "-OsaveOriginalReads=true" --report "${1}.report" --export "-v" $2 $3 $1

    mixcr exportClones -v "${1}.clna" "${1}_clones.txt"
}

declare -a wells=("A1" "B1" "C1" "D1" "E1" "F1" "G1" "H1" "A2" "B2" "C2" "D2" "E2" "F2" "G2" "H2")

for id in "${wells[@]}"
do
    echo $id
    run_mixcr "$id" "${id}_R1.fastq.gz" "${id}_R2.fastq.gz"
    run_mixcr "${id}_overlapping" "${id}_R12.fastq.gz"
done

# combine exported clones into one file
conda activate base # base must be py3.8
python3.8 combine_clones.py

exit
