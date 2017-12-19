"""Common tests using the toy data."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import basename

import pytest

from specio import specread
from specio.core import Spectrum
from specio.datasets import load_fsm_path
from specio.datasets import load_spc_path


@pytest.mark.parametrize(
    "filename,spectrum_shape,wavelength_shape",
    [(load_fsm_path(), (7998, 1641), (1641,)),
     (load_spc_path(), (1911,), (1911,))])
def test_toy_data(filename, spectrum_shape, wavelength_shape):
    spec = specread(filename)
    assert isinstance(spec, Spectrum)
    assert spec.amplitudes.shape == spectrum_shape
    assert spec.wavelength.shape == wavelength_shape
    assert spec.meta['filename'] == basename(filename)
