#!/bin/bash
set -e
set -o pipefail
set -u 

## Index genomes using the usual suspects (additional add routines can
## be added). All indexers must be in $PATH

REF=$1
REF_BASENAME=$(basename $REF .fa.gz)

## Bowtie2
bowtie2-build $REF $REF_BASENAME-bowtie2 &

## BWA Mem
bwa index $REF &
wait

## Novoalign
novoindex -k 14 -s 1 -t 10 $REF_BASENAME-novoalign $REF
