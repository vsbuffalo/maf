## dwgsim_eval.R -- evaluate dwgsim_eval's results in R
library(ggplot2)

PARFILE.MATCH <- "(\\w+)_([0-9abcdef]+).txt"

par.cols <- c("map.file", "hash", "command", "parameters")

dwgsim.cols <- list(
    min.mapping.quality="the minimum mapping quality threshold",
    n.reads.mapped.correctly.at.thresh="the number of reads mapped correctly that should be mapped at the threshold",
    n.reads.mapped.incorrectly.at.thresh="the number of reads mapped incorrectly that should be mapped be mapped at the threshold",
    n.reads.unmapped.at.thresh="the number of reads unmapped that should be mapped be mapped at the threshold",
    n.reads.mapped.should.be.unmapped.at.thresh="the number of reads mapped that should be unmapped be mapped at the threshold",
    n.reads.unmapped.should.be.unmapped.at.thresh="the number of reads unmapped that should be unmapped be mapped at the threshold",
    total.n.reads.mapped.at.thresh="the total number of reads mapped at the threshold",
    n.reads.mapped.correct.ge.thresh="the number of reads mapped correctly that should be mapped at or greater than that threshold",
    n.reads.mapped.incorrect.ge.thresh="the number of reads mapped incorrectly that should be mapped be mapped at or greater than that threshold",
    n.reads.unmapped.should.be.mapped.ge.thresh="the number of reads unmapped that should be mapped be mapped at or greater than that threshold",
    n.reads.mapped.should.be.unmapped.ge.thresh="the number of reads mapped that should be unmapped be mapped at or greater than that threshold",
    n.reads.unmapped.should.be.unmapped.ge.thresh="the number of reads unmapped that should be unmapped be mapped at or greater than that threshold",
    total.n.reads.mapped.ge.thresh="the total number of reads mapped at or greater than the threshold",
    sensitivity="the fraction of reads that should be mapped that are mapped correctly at the threshold",
    ppv="the fraction of mapped reads that are mapped correctly at the threshold",
    fdr="the fraction of random reads that are mapped at the threshold",
    sensitivity.ge.thresh="the fraction of reads that should be mapped that are mapped correctly at or greater than the threshold",
    ppv.ge.thresh="the fraction of mapped reads that are mapped correctly at or greater than the threshold",
    fdr.ge.thresh="the fraction of random reads that are mapped at or greater than the threshold")

# quick test no redundant columns
stopifnot(all(!duplicated(names(dwgsim.cols))))

readDwgsimEval <-
# read in single dwgsim eval files.
function(file) {
    tmp <- readLines(file)
    comments <- grep("^#.*", tmp)
    tmp <- lapply(tmp[-comments], function(x)
                  as.numeric(unlist(strsplit(x, split=" +"))))
    d <- as.data.frame(do.call(rbind, tmp))
    colnames(d) <- names(dwgsim.cols)
    d
}

.getAligner <- function(filenames) unlist(strsplit(gsub(PARFILE.MATCH, "\\1", filenames), ";;;"))
.getHash <- function(filenames) unlist(strsplit(gsub(PARFILE.MATCH, "\\2", filenames), ";;;"))


.loadEvalFiles <-
# data munging and combining of the actual dwgsim files.
function(dir, include.hashes) {
    # list all dwgsim eval files, and extract hash and aligner
    fnames <- list.files(dir, pattern="*.txt")
    info.d <- data.frame(filenames=fnames,
                         paths=list.files(dir, pattern="*.txt", full.names=TRUE),
                         hashes=.getHash(fnames),
                         aligners=.getAligner(fnames), stringsAsFactors=FALSE)
                         
    include <- hashes %in% include.hashes
    info.d <- subset(info.d, info.d$hashes %in% include.hashes)
    
    # read in dwgsim evaluation files
    d.eval <- do.call(rbind, mapply(function(x, n, a, h) {
        tmp <- readDwgsimEval(x)
        tmp$hash <- h
        tmp$aligner <- a
        tmp
    }, info.d$paths, info.d$filenames, info.d$aligners, info.d$hashes, SIMPLIFY=FALSE))
    d.eval
}

loadEval <-
# load and combine all dwgsim_eval files, make sure these match up to
# the run's parameter file.
function(parameter.file, dir="eval") {
    d.par <- read.delim(parameter.file, col.names=par.cols,
                        stringsAsFactors=FALSE)

    # in some cases, our eval file may have additional run data,
    # without hashes in the parameter file. Prune these.
    d.eval <- .loadEvalFiles(dir, d.par$hash)

    d.eval$command <- d.par$command[match(d.eval$hash, d.par$hash)]
    d.eval$parameters <- d.par$parameters[match(d.eval$hash, d.par$hash)]
    d.eval
}

