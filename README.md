0;95;c# MAF - Mapping Assessment Framework

MAF is a light framework to pipeline short read mapper/aligner
testing.

## Goals

 - Drop-in aligner testing: simple write a standard Unix configure
   file (see `bwa-mem.cfg` for an example) with the aligner, its path,
   version, command, reference, and evaluator, and which parameters
   you wish to test it across.

 - Wraps read simulators and corresponding evalution, so it goes
   directly to graphics.

 - Memoize entry values and input data so that things are not
   needlessly re-run when a new parameter is thrown in.

 - Entirely streaming summarization, i.e. the assessment
   takes SAM/BAM output directly from the aligner and assess it, to
   avoid clogging the disk with large file and having to worry about
   disk space and disk usage.

 - Works with clusters (SLURM) or simple parallelization with GNU
   parallel.

## Implementation

Currenty MAF is run like so:

    $ python maf/maf.py map -o test-run-1.txt -1 in1.fq -2 in2.fq bowtie2.cfg bwa-mem.cfg novoalign.cfg

This write a list of all commands to standard out, and writes an
output file `test-run-1.txt` which is a tab-delimited file that
contains the config file name, the hash, and the command for each run.

In future runs, you may wish to augment your past runs's results
(since these take a while to run). It's possible to only generate
commands that are new by
[http://en.wikipedia.org/wiki/Memoize](memoizing) past parameters that
have been run.

The commands output to standard out can than easily be run in GNU
parallel or SGE/SLURM via shell scripts.

## Pre-Run Checks

You will need to ensure the followning are true befor a MAF run:

1. All programs are installed, in `$PATH`, or the aligner runner
   script `scripts/alnrun.sh` are copied and adjusted for your
   environment.

2. All references are in place, **and indexed by each aligner you are
   running**.

3. You have enough space, memory, and computing power. Warning
   parameter spaces are large.
