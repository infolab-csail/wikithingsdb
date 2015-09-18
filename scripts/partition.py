import argparse
import codecs
import logging

logger = logging.getLogger(__name__)


def main(args, loglevel):
    # set up logging
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    file = codecs.open(args.file, 'r', 'utf-8')
    total = 0

    if args.output.endswith('/'):
        outfile_prefix = args.output + args.prefix
    else:
        outfile_prefix = args.output + '/' + args.prefix

    outfiles = [codecs.open('%s%s' % (outfile_prefix, i), 'w', 'utf-8')
                for i in xrange(args.number)]

    article = ''
    for line in file:
        article += line
        if line == '</doc>\n':
            outf = outfiles[total % args.number]
            outf.write(article)
            total += 1
            article = ''

    file.close()
    [f.close() for f in outfiles]
    logger.info('Finished partitioning %d articles into %d partitions' %
                (total, args.number))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Partitions a file generated by WikiExtractor",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-f",
        "--file",
        help="Path to path to merged xml file made with merge_extracted.sh",
        required=True,
        type=str
    )

    parser.add_argument(
        "-n",
        "--number",
        help="number of partitions",
        required=True,
        type=int
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output directory",
        required=True,
        type=str
    )

    parser.add_argument(
        "-p",
        "--prefix",
        help="Prefix for output files (default: partition-)",
        default="partition-",
        type=str
    )

    args = parser.parse_args()

    loglevel = logging.INFO
    main(args, loglevel)