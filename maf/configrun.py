# configrun.py -- holds ConfigRun class

HASHLENGTH=7

def make_hash_key(key):
    return hashlib.sha224(key).hexdigest()[:HASHLENGTH]

class ConfigRuns(object):
    """
    ConfigRuns are a class that take a set of configurations from an
    CFG file and turn these into a set of commands to run.
    """
    
    def __init__(self):
        """
        Initialize a ConfigSet, given a template
        """
        self.name = None
        self._parameters = dict()
        self._flags = dict()
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
        try:
            for field, value in config.items('flags'):
                value = re.split(r", *", value)
                self._flags[field] = value
        except ConfigParser.NoSectionError:
            pass
        self.name = config.get('program', 'name')
        self.path = config.get('program', 'path')
        self.version = config.get('program', 'version')
        self.ref_name = config.get('reference', 'ref')
        self.ref_path = config.get('reference', 'path')
        self.command = config.get('run', 'command')
        self.evaluator = config.get('evaluator', 'command')
        
    @property
    def command_args(self):
        """
        Return parameters in 
        """
    

    @property
    def arguments(self):
        """A dictionary of static arguments for this run (i.e. name, version,
        path, etc. that are used in the command.
        """
        return dict(name=self.name, path=self.path, version=self.version, ref=self.fullref, )

    @property
    def fullref(self):
        """
        Full reference (path plus name).
        """
        return path.join(self.ref_path, self.ref_name)
    
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

    def hashkeys(self, argdict):
        """Generate a set of hashkeys for a given argdict and parameters;
        also includes aligner name, and version.
        """
        tmp_hash_set = set()
        for command in self.commands(argdict):
            keyhash = " ".join([self.name, self.fullref, self.version, make_hash_key(key)])
            assert (keyhash not in tmp_hash_set) # collision check
            tmp_hash_set.add(keyhash)
            yield keyhash            

    def commands(self, argdict):
        """Make a set of all commands from the parameters by using
        `self._template` and the non-configured arguments in `argdict`. 
        """
        for paramset in self.parameter_strings:
            # build a dictionary with the constant arguments and
            # this particular set of parameters
            tmpdict = dict(argdict.items() + [("parameters", paramset)])
            yield string.Formatter().format(self.command, **tmpdict)

    def command_items(self, argdict):
        """
        Iterate through (hash, command) tuples.
        """
        for command in self.commands(argdict):
            yield (self._hash(command), command)
