from Indexer import Indexer
import argparse
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Index words in '
        'a preprocessed document and searchs for requested keywords.')
    parser.add_argument('original', help='Orginial text document')
    parser.add_argument('preprocessed', help='Preprocessed text document')
    parser.add_argument('--index ', dest='indexed', help='Writes list of '
                        'index words into the given file on quit.')
    parser.add_argument('--map ', dest='map_type', help='Uses given'
                        'data structures to index words. Available options are'
                        'avl, unsorted, sorted, chain, probe, splay, rb, dict,'
                        ' and od.')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args:
        indexer = Indexer(args.original, args.preprocessed, args.indexed,
                          args.map_type)
        indexer.index()
        print(indexer)
        indexer.startUI()
        indexer.dump()
    else:
        parser.print_help()