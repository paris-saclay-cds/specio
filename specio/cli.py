from __future__ import print_function

import os

from . import specread


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='specio',
        description='Python input/output for spectroscopic files')

    subparsers = parser.add_subparsers(metavar='', dest='sub')

    convert_parser = subparsers.add_parser(
        'convert',
        description='Convert spectroscopic files.',
        help='Convert spectroscopic files.')

    convert_parser.add_argument(
        'filepath', help='The file to convert.')

    convert_parser.add_argument(
        '--output', '-o', nargs=1,
        help='The output file path. If not specified, use same path and name '
             'as input with different extension.')

    args = parser.parse_args()

    if args.sub == 'convert':
        spectrum = specread(args.filepath)
        if args.output:
            output_path = args.output[0]
        else:
            output_path = os.path.splitext(args.filepath)[0] + '.csv'

        spectrum.to_csv(output_path)
        print("Written {}".format(output_path))
