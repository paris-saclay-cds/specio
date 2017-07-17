"""Test the user-facing API functions."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import join, dirname

from numpy.testing import assert_array_equal

from specio import help, read, specread
from specio.testing import assert_raises_regex

DATA_PATH = module_path = dirname(__file__)
RELATIVE_TOLERANCE = 1e-4


def test_help():
    # Test help(), it prints stuff, so we just check whether that goes ok
    help()  # should print overview
    help('FOOBAR')  # should print about PNG


def test_read():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R1 = read(filename)
    R2 = read(filename, 'foobar')
    assert R1.format == R2.format
    filename = join(DATA_PATH, 'data', 'spectra.notavalidext')
    assert_raises_regex(ValueError, "Could not find a format to read the"
                        " specified file", read, filename)
    assert_raises_regex(IOError, "No such file", read, 'notexisting.barf')
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    assert_raises_regex(IndexError, "No format known by name", read, filename,
                        'notexistingformat')


def test_specread():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    spec1 = specread(filename)
    spec2 = specread(filename, 'foobar')
    assert spec1.spectrum.shape == (1, 801)
    assert spec1.wavelength.shape == (801,)
    assert_array_equal(spec1.spectrum, spec2.spectrum)
    assert_array_equal(spec1.wavelength, spec2.wavelength)
