# MAF - Mapping Assessment Framework

MAF is a light framework to pipeline short read mapper/aligner
testing.

## Goals

 - Drop-in aligner testing: simple write a standard Unix configure
   file (see `bwa-mem.cfg` for an example) with the aligner, its path,
   version, subcommand, and which parameters you wish to test it
   across. MAF generates a SLURM script that can be run across many

 - Wraps read simulators and corresponding evalution (since some
   simulators like wgsim use FASTQ headers for information on where
   the reads originate from.

 - Memoize entry values so that things are not needlessly re-run when
   a new parameter is thrown in.

 - Optional entirely streaming summarization, i.e. the assessment
   takes SAM/BAM output directly from the aligner and assess it, to
   avoid clogging the disk with large file and having to worry about
   disk space and disk usage.

 - Works with clusters (SLURM) or simple parallelization with GNU
   parallel.

## Implementation

