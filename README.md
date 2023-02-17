# antigenReceptorRepertoires
Analysis of bulk and single-cell TCR and BCR libraries

## Requirements
- [MiGEC](https://migec.readthedocs.io/en/latest/index.html)
- [MiXCR](https://github.com/milaboratory/mixcr)
- [VDJtools](https://vdjtools-doc.readthedocs.io/en/master/#)
- [OLGA](https://github.com/statbiophys/OLGA)

## Manifest
`TCR_demultiplex.sh`, `BCR_demultiplex.sh`: use MiGEC and MiXCR to demultiplex paired-end reads from Illumina sequencing and align TCRs or BCRs.

`readStats.py`: Determines for single-cell plateseq experiment, such as FACS-sorted single cells, the clonal read count per well.
<p align="center">
<img src="well_counts.png" height=50% width=50>
</p>

`blankProportion.py`: determines the proportion of blank reads as a function of clone read count. Useful for determining the optimal read count cutoff.
<p align="center">
<img src="proportionBlank_vs_reads.png" height=50% width=50>
</p>
