#!/bin/bash
# Script for demultiplexing 2x250bp Illumina reads with index sequences on 3' end,
# and running mixcr to get final BCR sequences

source /opt/anaconda3/etc/profile.d/conda.sh # required to be able to activate conda env in subshell

conda create -n r-environment r-essentials r-base
conda activate r-environment
pip install brew
brew install java

#activate env
conda activate r-environment

# make sure you have ~/migec*/migec*.jar
# demultiplex
SAMPLE="S1" #change based on your sample prefix

mkdir ${SAMPLE}_demultiplexed
cp combine_clones.py ./${SAMPLE}_demultiplexed

java -jar ~/migec*/migec*.jar Checkout -cut --overlap --rc-barcodes barcode_migec.txt ${SAMPLE}_R1_001.fastq.gz ${SAMPLE}_R2_001.fastq.gz ./${SAMPLE}_demultiplexed
cd ./${SAMPLE}_demultiplexed

# Run mixcr on paired reads from Amplicon-EZ seq of PCR products

run_mixcr () {
    mixcr analyze amplicon -s hsa --starting-material rna --5-end v-primers --3-end c-primers --adapters adapters-present --receptor-type bcr --contig-assembly --align "-OsaveOriginalReads=true" --report "${1}.report" --export "-v" $2 $3 $1

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
python3.8 combine_clones.py # see other gist

exit
