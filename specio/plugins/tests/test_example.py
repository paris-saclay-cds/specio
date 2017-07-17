"""Test the example plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join

from specio import formats
from specio.core import Request

DATA_PATH = module_path = dirname(__file__)


def test_dummy_format():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')

    R = Request(filename, 's')
    F = formats['FOOBAR']
    assert F.can_read(R)
    reader = F.get_reader(R)
    assert reader.get_length() == 1
    assert reader.get_meta_data() == {}
    spec = reader.get_data(0)
    assert spec._spectrum.shape == (1, 801)
    assert spec._wavelength.shape == (801,)
