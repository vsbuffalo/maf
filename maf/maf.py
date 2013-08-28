import ConfigParser

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='maf')
    subparsers = parser.add_subparsers(help="sub-commands")
    parser_sim = subparsers.add_parser('sim', help="")
    parser_j = subparsers.add_parser('sim', help="")

parser.add_subparsers(title="subcommands"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("-u", "--unphased",
                        help="FASTA filename for reads from unphased contigs",
                        type=argparse.FileType('w'), default=None, required=False)
