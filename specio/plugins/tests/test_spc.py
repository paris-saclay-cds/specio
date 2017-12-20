"""Test the SPC plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join

import pytest

from specio import specread


DATA_PATH = dirname(__file__)


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
            assert spec[wi].amplitudes.shape == spectrum_shape[wi]
            assert spec[wi].wavelength.shape == wavelength_shape[wi]
    else:
        assert spec.amplitudes.shape == spectrum_shape
        assert spec.wavelength.shape == wavelength_shape
