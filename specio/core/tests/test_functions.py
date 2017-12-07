"""Test the user-facing API functions."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import join, dirname

import pytest

from numpy.testing import assert_allclose

from specio import help, read, specread

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


@pytest.mark.parametrize("type_error,msg, filename,file_format",
                         [(ValueError, "Could not find a format",
                           join(DATA_PATH, 'data', 'spectra.notavalidext'),
                           None),
                          (IOError, "No such file", "notexisting.barf", None),
                          (IndexError, "No format known by name",
                           join(DATA_PATH, 'data', 'spectra.foobar'),
                           'notexistingformat')])
def test_read_error(type_error, msg, filename, file_format):
    with pytest.raises(type_error, message=msg):
        read(filename, format=file_format)


def test_specread():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    spec1 = specread(filename)
    spec2 = specread(filename, 'foobar')
    assert spec1.spectrum.shape == (1, 801)
    assert spec1.wavelength.shape == (801,)
    assert_allclose(spec1.spectrum, spec2.spectrum)
    assert_allclose(spec1.wavelength, spec2.wavelength)
