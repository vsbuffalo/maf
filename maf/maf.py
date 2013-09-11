import ConfigParser
import re
from itertools import product
from collections import namedtuple

TEST = True

if TEST:
    import pdb

def remove_dashes(string):
    re.replace

class ConfigRuns(object):
    """
    ConfigRuns are a class that take a set of configurations from an
    CFG file and turn these into a set of commands to run.
    """
    
    def __init__(self, template=None):
        """
        Initialize a ConfigSet, given a template
        """
        self.name = None
        self._template = template
        self._parameters = dict()
        self.ref_name = None
        self.ref_path = None
        self.path = None
        self.version = None
        self.command = None
        

    def readfp(self, fp):
        """Parse the config file at `fp`, building a ConfigRun object for a
        specific set of configurations given in the CFG file.
        """
        config = ConfigParser.ConfigParser()
        config.readfp(fp)
        for field, value in config.items('parameters'):
            # split parameter vector into chunks
            value = re.split(r", *", value)
            self._parameters[field] = value
        self.name = config.get('program', 'name')
        self.path = config.get('program', 'path')
        self.version = config.get('program', 'version')
        self.ref_name = config.get('reference', 'ref')
        self.ref_path = config.get('reference', 'path')
        self.command = config.get('run', 'command')                
    
    @property
    def parameters(self):
        """
        Return a itertools.product object of all parameter combinations.
        """
        params = list()
        for key, value in self._parameters.items():
            params.append(["%s %s" % (key, v) for v in value])
        return product(*params)

    def runkey(self, parameters):
        """For a single run configuration, generate a key that hashes all
        information.
        """

        

    def commands(self, argdict):
        """Make a set of all commands from the parameters by using
        `self._template` and the non-configured arguments in `argdict`. 
        """
        try:
            string.Formatter().format(self._template, **argdict)
        except KeyError(e):
            pdb.set_trace()
            
        
        

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='maf')
    subparsers = parser.add_subparsers(help="sub-commands")
    parser_dwgsim = subparsers.add_parser('dwgsim', help="")
    parser_dwgsim.add_argument("-s", "--seed", 
                              help="seed, specify many arguments for many simulated read sets", 
                              nargs="+", type=int)
    parser_map = subparsers.add_parser('map', help="generate a script to run an alignment")
    parser_map.add_argument("simfile", type=argparse.FileType('r'), 
                            help="config file returned from dwgsim")
    parser_map.add_argument("mapfile", type=argparse.FileType('r'), 
                            help="aligner config file the specifies which parameters to test")
    
    if TEST:
        a = ConfigRuns()
        a.readfp(open("bwa-mem.cfg"))
