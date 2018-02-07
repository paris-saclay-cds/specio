"""Test the user-facing API functions."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import join, dirname

import pytest

import numpy as np
from numpy.testing import assert_allclose

from specio import help, get_reader, specread
from specio.core import Spectrum

DATA_PATH = dirname(__file__)
RNG = np.random.RandomState(0)


def test_help():
    # Test help(), it prints stuff, so we just check whether that goes ok
    help()  # should print overview
    help('FOOBAR')  # should print about PNG


def test_get_reader():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R1 = get_reader(filename)
    R2 = get_reader(filename, 'foobar')
    assert R1.format == R2.format


@pytest.mark.parametrize(
    "type_error,msg, filename,file_format",
    [(ValueError, "Could not find a format",
      join(DATA_PATH, 'data', 'spectra.notavalidext'), None),
     (IOError, "No such file", "notexisting.barf", None),
     (IndexError, "No format known by name",
      join(DATA_PATH, 'data', 'spectra.foobar'), 'notexistingformat')])
def test_get_reader_error(type_error, msg, filename, file_format):
    with pytest.raises(type_error, message=msg):
        get_reader(filename, format=file_format)


def test_specread_single_file():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    spec1 = specread(filename)
    spec2 = specread(filename, 'foobar')
    assert spec1.amplitudes.shape == (1, 801)
    assert spec1.wavelength.shape == (801,)
    assert_allclose(spec1.amplitudes, spec2.amplitudes)
    assert_allclose(spec1.wavelength, spec2.wavelength)


def _generate_spectrum_identical_wavelength(*args):
    """Generate spectrum with identical wavelength."""
    n_wavelength = 5
    return Spectrum(np.random.random_sample(n_wavelength),
                    np.arange(n_wavelength),
                    None)


def _generate_spectrum_different_wavelength_size(*args):
    """Generate spectrum with different wavelength size."""
    n_wavelength = np.random.randint(10, 20)
    return Spectrum(np.random.random_sample(n_wavelength),
                    np.arange(n_wavelength),
                    None)


def _generate_spectrum_different_wavelength(*args):
    """Generate spectrum with identical wavelength."""
    n_wavelength = 5
    return Spectrum(np.random.random_sample(n_wavelength),
                    np.random.permutation(np.arange(n_wavelength)),
                    None)


def _generate_list_spectrum(*args):
    """Generate spectrum with identical wavelength."""
    n_spectrum = RNG.randint(1, 5)
    n_wavelength = 5
    return [Spectrum(np.random.random_sample(n_wavelength),
                     np.arange(n_wavelength),
                     None)
            for _ in range(n_spectrum)]


def _generate_list_spectrum_close_wavelength(*args):
    n_wavelength = 5
    tol = 1e-3
    wavelength = np.arange(5) + np.random.uniform(low=-tol, high=tol)
    return Spectrum(np.random.random(n_wavelength),
                    wavelength,
                    None)


@pytest.mark.parametrize(
    "side_effect,tol_wavelength,spectra_type,spectra_shape",
    [(_generate_spectrum_identical_wavelength, 1e-5, Spectrum, (10, 5)),
     (_generate_spectrum_different_wavelength_size, 1e-5, list, 10),
     (_generate_spectrum_different_wavelength, 1e-5, list, 10),
     (_generate_list_spectrum, 1e-5, list, 30),
     (_generate_list_spectrum_close_wavelength, 1e-2, Spectrum, (10, 5)),
     (_generate_list_spectrum_close_wavelength, 1e-5, list, 10)])
def test_specread_consitent_wavelength(side_effect, tol_wavelength,
                                       spectra_type, spectra_shape, mocker):
    # emulate that we read several file
    mocker.patch('specio.core.functions._validate_filenames',
                 return_value=['filename' for _ in range(10)])

    mocker.patch('specio.core.functions._get_reader_get_data',
                 side_effect=side_effect)

    # emulate the spectrum reading
    spectra = specread('', tol_wavelength=tol_wavelength)
    assert isinstance(spectra, spectra_type)
    if isinstance(spectra, Spectrum):
        assert spectra.amplitudes.shape == spectra_shape
        assert spectra.wavelength.shape == (spectra_shape[1],)
        assert spectra.meta == tuple({} for _ in range(spectra_shape[0]))
    elif isinstance(spectra, list):
        assert len(spectra) == spectra_shape
