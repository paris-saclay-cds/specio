from __future__ import print_function

from . import specread


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='specio',
        description='Convert spectroscopic files.')

    parser.add_argument(
        'filepath', help='The file to convert.')

    parser.add_argument(
        '--output', '-o', nargs=1,
        help='The output file path. If not specified, use same path and name '
             'as input with different extension.')

    args = parser.parse_args()

    spectrum = specread(args.filepath)
    print(spectrum)
    print(args.output)
