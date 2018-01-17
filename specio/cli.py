from __future__ import print_function

from . import specread


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='specio',
        description='Convert spectroscopic files.')

    parser.add_argument(
        'filepath', help='The file to convert.')

    args = parser.parse_args()

    spectrum = specread(args.filepath)
    print(spectrum)
