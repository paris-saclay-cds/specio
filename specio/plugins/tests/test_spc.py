"""Test the SPC plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from specio import formats
from specio.core import Request
from specio.datasets import load_spc_path


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
