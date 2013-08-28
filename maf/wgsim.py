"""
wgsim.py -- Functions to handle output from the wgsim parser. 

Note: wgsim gives 0-based coordinates, SAM is 1-based, and BAM is
0-based. Luckily pysam abstracts away from the SAM/BAM difference 
and everything is 0-based.
"""
import re
import pysam
import pdb

# These are wgsim's sequence header fields, drawn from wgsim.c. These
# are the same across readpairs
WGSIM_MATCHER = re.compile(r"^(?P<seqname>[\w-]+)_(?P<pos1>\d+)_(?P<pos2>\d+)_"
                           "(?P<nerr1>\d+):(?P<nsub1>\d+):(?P<nindel1>\d+)_"
                           "(?P<nerr2>\d+):(?P<nsub2>\d+):(?P<nindel2>\d)_(?P<id>\d)/(?P<pair>[12])")

# storage for Simulated Read field values
SimRead = namedtuple("SimRead", ["seqname", "pos", "id", "nerr", "nsub", "nindel", "pair"])

def parse_wgsim_header(header):
    """
    Parse a header ID (read name) into the position from the genome it
    was simulated from.

    Then, merge the read pair's values into a tuple.

    """
    match = WGSIM_MATCHER.match(header)
    if match is None:
        raise ValueError, "cannot parse '%s' - was this generated from wgsim?" % header
    wf = dict()
    tmp = match.groupdict()
    wf["seqname"] = tmp["seqname"]
    wf["pair"] = tmp["pair"]
    wf["id"] = int(tmp["id"], 16)
    for field in ("pos", "nerr", "nsub", "nindel"):
        wf[field] = (tmp[field+"1"], tmp[field+"2"])
    return SimRead(wf["seqname"], wf["pos"], wf["id"], wf["nerr"], wf["nsub"], wf["nindel"], wf["pair"])

def eval_alignments(samfile):
    """Parse an AlignedRead object from pysam and check it against a
    header from wgsim to see if it's aligned properly.

    Much of the logic is adapted from wgsim_eval.pl. We want to return 
    values like:
      - distance away from true position for each read of pair
      - number clipped
      - mapping quality
      - mismatches (NM tag compared to read error and substitutions)

    Notes:
    
    1) AlignedRead.pos is first aligned base, not positions of
    where beginning of read would be. AlignedRead.aend is the
    reference position where the alignment ends (and not necessarily
    AlignedRead.pos + read_length since CIGAR string can have H/S
    clipping or deletions from ref.

    2) The coordinates give by wgsim are the *fragment
    coordinates*. Thus the reported insert size is the distance
    between the wgsim coordinates.

    3) A reverse read is either the forward read of a fragment on the
    opposite strand (1) or the reverse read of a forward fragment (2):

        /---1---
    |-------------------------| (1)
                   ---2---/

                      ---2---/
    |-------------------------| (2)
          /---1---

    Heng's wgsim_eval.pl takes the approach that since the insert size
    > gap (where a correct alignment is where (position - actual <
    gap), then an alignment is *incorrect* if both read ends are
    further than gap. As far as I can tell this is so that read pairs
    don't need to be processed together.

    """
    stats = Counter()
    total = 0
    pos_diff = list(Counter(), Counter())
    for read in samfile:
        wgsim_fields = parse_wgsim_header(read.qname)

        if read.is_unmapped:
            stats["unmapped"] += 1
            continue
        if samfile.getrname(reads.tid) != wgsim_fields.seqname:
            stats[""]
        if read.is_reverse:
            
            
