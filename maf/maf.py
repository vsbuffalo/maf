import ConfigParser
import re
from itertools import product
from collections import namedtuple
import hashlib
import string
from operator import itemgetter

# for debugging/testing
TEST = True

if TEST:
    import pdb

# import primary class, ConfigRuns
from configrun import ConfigRuns

def create_aligner_runs(args):
    """
    Create an aligner run.
    """
    aligner_runs = dict()
    param_spaces = dict()
    for config_file in args.mapfiles:
        run = ConfigRuns()
        with open(config_file) as config_fp:
            run.readfp(config_fp)
        for hashkeys, command in run.command_items():
            param_spaces[config_file] += 1
            if not arg.size:
                args.output_file.write("\t".join(config_file, hashkeys, command) + "\n")
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
    parser_map.add_argument("mapfiles", type=argparse.FileType('r'), nargs="+",
                            help="aligner config file the specifies which parameters to test")
    parser_map.add_argument("-o", "--output-file", type=argparse.FileType('w'),
                            help="parameter output file (links file names with parameters)")
    parser_map.add_argument("-1", help="simulated read pair 1")
    parser_map.add_argument("-2", help="simulated read pair 2")
    parser_map.add_argument("-s", "--size", help="return the parameter space and exit", action="store_true")
    parser_map.set_defaults(func=create_aligner_runs)
    args = parser.parse_args()
    args.func(args)

    

    
    if TEST:
        a = ConfigRuns()
        a.readfp(open("bwa-mem.cfg"))
        run_args = dict(ref="test.fa", in1="read1.fq", in2="read2.fq", out="out.sam", log="log.stderr")
        commands = a.commands(run_args)

        s = ConfigRuns()
        s.readfp(open("dwgsim.cfg"))
        run_args = dict()
        commands = a.commands(run_args)

