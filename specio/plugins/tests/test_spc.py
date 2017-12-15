"""Test the SPC plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join

import pytest

from specio import specread
from specio import formats
from specio.core import Request
from specio.core import Spectrum
from specio.datasets import load_spc_path


DATA_PATH = dirname(__file__)


def test_spc_format():
    filename = load_spc_path()

    R = Request(filename)
    F = formats['SPC']
    assert F.can_read(R)
    reader = F.get_reader(R)
    assert reader.get_length() == 1
    assert reader.get_meta_data()['dat_fmt'] == 'x-y'
    spec = reader.get_data()
    assert spec.spectrum.shape == (1911,)
    assert spec.wavelength.shape == (1911,)
    spec = reader.get_data(0)
    assert spec.spectrum.shape == (1911,)
    assert spec.wavelength.shape == (1911,)


@pytest.mark.parametrize(
    "filename,spectrum_shape,wavelength_shape",
    [(join(DATA_PATH, 'data', 'spc', 'single_file', 'gxy.spc'),
      (151,), (151,)),
     (join(DATA_PATH, 'data', 'spc', 'single_file', 'x-y.spc'),
      (31, 1024), (1024,)),
     (join(DATA_PATH, 'data', 'spc', 'single_file', '-xy.spc'),
      [(8,), (6,)], [(8,), (6,)])])
def test_spc_file(filename, spectrum_shape, wavelength_shape):
    spec = specread(filename)
    if isinstance(spec, list):
        # in '-xy.spc', there is two different wavelength size: we are checking
        # each of them
        for wi in range(1):
            assert spec[wi].spectrum.shape == spectrum_shape[wi]
            assert spec[wi].wavelength.shape == wavelength_shape[wi]
    else:
        assert spec.spectrum.shape == spectrum_shape
        assert spec.wavelength.shape == wavelength_shape


@pytest.mark.parametrize(
    "filename,spectrum_type,spectrum_shape",
    [(join(DATA_PATH, 'data', 'spc', 'homogeneous_wavelength', '*.spc'),
      Spectrum, (2, 1911)),
     (join(DATA_PATH, 'data', 'spc', 'heterogeneous_wavelength', '*.spc'),
      list, 514),
     (join(DATA_PATH, 'data', 'spc', 'single_file', '*.spc'), list, 514)])
def test_multiple_spc_files(filename, spectrum_type, spectrum_shape):
    spec = specread(filename)
    assert isinstance(spec, spectrum_type)
    if isinstance(spec, Spectrum):
        assert spec.spectrum.shape == spectrum_shape
    elif isinstance(spec, list):
        assert len(spec) == spectrum_shape
