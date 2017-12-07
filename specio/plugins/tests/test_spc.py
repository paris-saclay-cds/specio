"""Test the SPC plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join

import pytest

from specio import specread
from specio import formats
from specio.core import Request
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
    assert spec.spectrum.shape == (1, 1911)
    assert spec.wavelength.shape == (1911,)
    spec = reader.get_data(0)
    assert spec.spectrum.shape == (1911,)
    assert spec.wavelength.shape == (1911,)


@pytest.mark.parametrize(
    "filename,spectrum_shape,wavelength_shape",
    [(join(DATA_PATH, 'data', 'gxy.spc'), (1, 151), (151,)),
     (join(DATA_PATH, 'data', 'x-y.spc'), (31, 1024), (1024,)),
     (join(DATA_PATH, 'data', '-xy.spc'), (1, 151), (151,))])
def test_spc_file(filename, spectrum_shape, wavelength_shape):
    spec = specread(filename)
    assert spec.spectrum.shape == spectrum_shape
    assert spec.wavelength.shape == wavelength_shape


def test_spc_xy():
    filename = join(DATA_PATH, 'data', 'gxy.spc')
    spec = specread(filename)

    assert spec.spectrum.shape == (1, 151)
    assert spec.wavelength.shape == (151,)
