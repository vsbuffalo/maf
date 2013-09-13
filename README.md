# MAF - Mapping Assessment Framework

MAF is a light framework to pipeline short read mapper/aligner
testing.

## Goals

 - Drop-in aligner testing: simple write a standard Unix configure
   file (see `bwa-mem.cfg` for an example) with the aligner, its path,
   version, subcommand, and which parameters you wish to test it
   across. MAF generates a SLURM script that can be run across many

 - Wraps read simulators and corresponding evalution, so it goes
   directly to graphics.

 - Memoize entry values so that things are not needlessly re-run when
   a new parameter is thrown in.

 - Entirely streaming summarization, i.e. the assessment
   takes SAM/BAM output directly from the aligner and assess it, to
   avoid clogging the disk with large file and having to worry about
   disk space and disk usage.

 - Works with clusters (SLURM) or simple parallelization with GNU
   parallel.

## Implementation

    $ maf map -o params.txt -1 read1.fq -2 read2.fq bwa-mem.cfg bowtie2.cfg | gnu parallel bash mapscript.sh
	$ maf join params.txt 

It's wise to see how large the parameter space is before running
MAF. This can be done with:

    $ maf map -s -1 read1.fq -2 read2.fq bwa-mem.cfg bowtie2.cfg


## Pre-Run Checks

You will need to ensure the followning are true befor a MAF run:

1. All programs are installed, in `$PATH`, or the aligner runner
   script `scripts/alnrun.sh` are copied and adjusted for your
   environment.

2. All references are in place, **and indexed by each aligner you are
   running**.

3. You have enough space, memory, and computing power. Warning
   parameter spaces are large.
