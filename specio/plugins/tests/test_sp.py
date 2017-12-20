"""Test the SP plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import pytest

from specio import formats
from specio.core import Request
from specio.datasets import load_sp_path


def test_sp_format():
    filename = load_sp_path()

    R = Request(filename)
    F = formats['SP']
    assert F.can_read(R)
    reader = F.get_reader(R)
    assert reader.get_length() == 3301
    assert reader.get_meta_data()['signature'] == b'PEPE'
    spec = reader.get_data()
    assert spec.spectrum.shape == (3301,)
    assert spec.wavelength.shape == (3301,)
    spec = reader.get_data(0)
    assert spec.spectrum.shape == (3301,)
    assert spec.wavelength.shape == (3301,)
    assert spec.spectrum[0] == pytest.approx(0.03723936007346753)
