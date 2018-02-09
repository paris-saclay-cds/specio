from __future__ import print_function

import os

import numpy as np

from .core.functions import _validate_filenames
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
        'filepath', help='The file to convert. Wildcard are accepted'
        ' (e.g. "*.spc")')

    convert_parser.add_argument(
        '--output', '-o', nargs=1,
        help='The output file path. If not specified, use same path and name '
             'as input with different extension.')

    convert_parser.add_argument(
        '--tolerance', '-t', nargs=1, type=float, default=[1e-5],
        help='Tolerance to merge spectrum when their wavelength are slightly '
             'different (default=1e-5)')

    args = parser.parse_args()

    if args.sub == 'convert':
        filenames = _validate_filenames(args.filepath)
        tol_wavelength = args.tolerance[0]
        spectrum = specread(filenames, tol_wavelength=tol_wavelength)

        # case that we could not merge the spectra together
        if isinstance(spectrum, list):
            if args.output:
                # remove the extension in case that the user gave one
                output_basename, _ = os.path.splitext(args.output[0])
                for idx, sp in enumerate(spectrum):
                    sp.to_csv(output_basename + '_{}.csv'.format(idx))
            else:
                output_basename = [sp.meta['filename'] for sp in spectrum]
                if np.unique(output_basename).size == len(output_basename):
                    for name, sp in zip(output_basename, spectrum):
                        sp.to_csv(os.path.splitext(name)[0] + '.csv')
                else:
                    basename = os.path.splitext(output_basename[0])[0]
                    for idx, sp in enumerate(spectrum):
                        sp.to_csv(basename + '_{}.csv'.format(idx))

        # case that we have a single spectrum
        else:
            if args.output:
                output_path = args.output[0]
            else:
                # we are using the first name as a basename
                output_path = os.path.splitext(filenames[0])[0] + '.csv'

            spectrum.to_csv(output_path)
            print("Written {}".format(output_path))
