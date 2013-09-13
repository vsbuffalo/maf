import re
import sys
from collections import Counter

# for debugging/testing
TEST = True

if TEST:
    import pdb

# import primary class, AlignerRun
from alignerrun import AlignerRun

def create_aligner_runs(args):
    """
    Create an aligner run.
    """
    aligner_runs = dict()
    param_spaces = Counter()
    for config_file in args.mapfiles:
        run = AlignerRun(args.in1, args.in2)
        with open(config_file) as config_fp:
            run.readfp(config_fp)
        for hashkeys, command in run.commands():
            param_spaces[config_file] += 1
            if not args.size:
                args.output_file.write("\t".join([config_file, hashkeys, command]) + "\n")
                sys.stdout.write(command + "\n")
        aligner_runs[config_file] = run

    if args.size:
        # return parameter space size and exit
        for config_file, size in param_spaces.items():
            print "\t".join([config_file, str(size)])
        sys.exit(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='maf')
    subparsers = parser.add_subparsers(help="sub-commands")
    # MAYBE have subcommands for different read aligners

    parser_map = subparsers.add_parser('map', help="generate a script to run an alignment")
    parser_map.add_argument("mapfiles", type=str, nargs="+",
                            help="aligner config file the specifies which parameters to test")
    parser_map.add_argument("-o", "--output-file", type=argparse.FileType('w'), required=True,
                            help="parameter output file (links file names with parameters)")
    parser_map.add_argument("-s", "--sam-path", type=str, default="alns/",
                            help="output path for alignment SAM files")
    parser_map.add_argument("-e", "--eval-path", type=str, default="eval/",
                            help="output path for evaluation files from dwgsim")
    parser_map.add_argument("-l", "--log-path", type=str, default="log/",
                            help="output path for standard error log")
    parser_map.add_argument("-1", "--in1", help="simulated read pair 1", required=True)
    parser_map.add_argument("-2", "--in2", help="simulated read pair 2", required=True)
    parser_map.add_argument("-S", "--size", help="return the parameter space and exit", action="store_true")
    parser_map.set_defaults(func=create_aligner_runs)
    args = parser.parse_args()
    args.func(args)
