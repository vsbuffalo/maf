# alignerrun.py -- holds AlignerRun class

import ConfigParser
from itertools import product
from collections import namedtuple
from os import path, curdir
from itertools import izip
import hashlib
import string
from operator import itemgetter
import re
import sys

HASHLENGTH=7
FORMATTERS = re.compile(r"{(\w+)}")

def make_hash_key(key):
    return hashlib.sha224(key).hexdigest()[:HASHLENGTH]

def make_name(name, hashkey, ext, *args):
    name = name.replace(' ', '_') # sanitize name
    assert(" " not in ext)
    if len(args) == 0:
        return "%s_%s.%s" % (name, hashkey, ext)
    else:
        other_info = "_".join([a.replace(' ', '_') for a in args])
        return "%s_%s_%s.%s" % (name, hashkey, other_info, ext)

class AlignerRun(object):
    """AlignerRun is a class that take a set of configurations from an
    CFG file and turn these into a set of commands to run.
    """
    
    def __init__(self, in1, in2, log_path=None, sam_path=None, eval_path=None, 
                 time_path=None, memoize_file=None):
        """
        Initialize a ConfigSet, given a template
        """
        self.name = None
        self.in1 = in1
        self.in2 = in2
        self._parameters = dict()
        self._flags = dict()
        self.ref_name = None
        self.ref_path = None
        self.time_path = time_path
        self.path = None
        self.version = None
        self.command = None
        self.evaluator = None
        self.sam_path = sam_path
        self.eval_path = eval_path
        self.log_path = log_path
        self.memoized_ids = set()
        if memoize_file is not None:
            with open(memoize_file) as f:
                for line in f:
                    self.memoized_ids.add(line.split("\t")[1])

    def readfp(self, fp):
        """Parse the config file at `fp`, building a AlignerRun object for a
        specific set of configurations given in the CFG file.
        """
        config = ConfigParser.ConfigParser()
        config.optionxform = str # prevent lowercase, which can screw up parameters
        config.readfp(fp)
        for field, value in config.items('parameters'):
            # split parameter vector into chunks
            value = re.split(r", *", value)
            self._parameters[field] = value
        try:
            for field, value in config.items('flags'):
                value = re.split(r", *", value)
                self._flags[field] = value
        except ConfigParser.NoSectionError:
            pass
        self.name = config.get('program', 'name')
        try:
            # path is optional
            self.path = config.get('program', 'path')
        except ConfigParser.NoOptionError:
            self.path = None
        self.version = config.get('program', 'version')
        self.ref_name = config.get('reference', 'ref')
        self.ref_path = config.get('reference', 'path')
        self.command = config.get('run', 'command')
        self.evaluator = config.get('evaluator', 'command')

    @property
    def run_command_args(self):
        """Return formatters in the run->command value.
        """
        return tuple(FORMATTERS.findall(self.command))
    
    @property
    def parameters(self):
        """Return a itertools.product object of all parameter and flag
        combinations.
        """
        params = list()
        for key, value in self._parameters.items():
            params.append(["%s %s" % (key, v) for v in value])
        for flags in self._flags.values():
            params.append(flags)
        return product(*params)

    @property
    def parameter_strings(self):
        """Parameters in string format to become command, returned a
        generator.
        """
        return (" ".join(params) for params in sorted(list(self.parameters)))
    
    @property
    def hashkeys(self):
        """Generate a set of hashkeys for the parameters space and few other
        bits of information including aligner name, and version.
        """
        tmp_hash_set = set()
        for params in self.parameter_strings:
            keyhash = make_hash_key(" ".join([self.name, self.ref_path, self.version, params]))
            assert (keyhash not in tmp_hash_set) # collision check, just in case
            tmp_hash_set.add(keyhash)
            yield keyhash

    def commands(self):
        """Make a set of all commands from the parameters by using
        `self._template` and the non-configured arguments in `argdict`. 

        command={program} -x {ref} {parameters} -1 {in1} -2 {in2} 2> {log} | tee {aln_out} | {evaluator} > {eval_out}
        """
        for hashkey, paramstr in izip(self.hashkeys, self.parameter_strings):
            if hashkey in self.memoized_ids:
                continue
            sam_out = path.join(self.sam_path, make_name(self.name, hashkey, "sam"))
            eval_out = path.join(self.eval_path, make_name(self.name, hashkey, "txt"))
            log_out = path.join(self.log_path, make_name(self.name, hashkey, "txt", "log"))
            time_out = path.join(self.time_path, make_name(self.name, hashkey, "txt", "time"))
            
            program = self.name if self.path is None else self.name
            
            # build a dictionary with the constant arguments and
            # this particular set of parameters
            tmpdict = dict(in1=self.in1, in2=self.in2, eval_out=eval_out, 
                           ref=self.ref_path, parameters=paramstr, program=program,
                           time_out=time_out,
                           sam_out=sam_out, log_out=log_out, evaluator=self.evaluator)
            
            try:
                yield (hashkey, string.Formatter().format(self.command, **tmpdict))
            except KeyError, e:
                args = ", ".join(e.args)
                sys.stderr.write("error: run->command formatter missing arguments: %s\n" % args)
                sys.exit()
