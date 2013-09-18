#!/bin/bash
#SBATCH -D /home/vince251/projects/maf-run
#SBATCH -o /home/vince251/projects/maf-run/logs/stdout-%j.txt
#SBATCH -e /home/vince251/projects/maf-run/logs/stderr-%j.txt
#SBATCH -J maf
set -e
set -u

function check_in_path() {
    command -v $1 >/dev/null 2>&1 || { echo >&2 "$1 required but not in $PATH"; exit 1; }
}

check_in_path dwgsim_eval
check_in_path novoalign
check_in_path bowtie2
check_in_path bwa

IN1=simreads/chr2-chr10-01.bwa.read1.fastq
IN2=simreads/chr2-chr10-01.bwa.read2.fastq
MAFPY=python /home/vince251/projects/maf/maf/maf.py

mkdir -p log
mkdir -p alns
mkdir -p eval

$MAFPY map -o mafrun-1.txt -1 $IN1 -2 $IN2 bowtie2.cfg bwa-mem.cfg novoalign.cfg | sed -n "$SLURM_ARRAY_TASK_ID"p | bash
