"""Test the FSM plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import pytest

from specio import formats
from specio import specread
from specio.core import Request
from specio.datasets import load_fsm_path


def test_fsm_format():
    filename = load_fsm_path()

    R = Request(filename)
    F = formats['FSM']
    assert F.can_read(R)
    reader = F.get_reader(R)
    assert reader.get_length() == 7998
    assert reader.get_meta_data()['signature'] == b'PEPE'
    spec = reader.get_data()
    assert spec.spectrum.shape == (7998, 1641)
    assert spec.wavelength.shape == (1641,)
    spec = reader.get_data(0)
    assert spec.spectrum.shape == (1641,)
    assert spec.wavelength.shape == (1641,)
    assert spec.spectrum[0] == pytest.approx(38.656551)
