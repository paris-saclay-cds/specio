"""Testing mzML plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import basename

import pytest

from specio import specread
from specio import formats
from specio.core import Request
from specio.core import Spectrum
from specio.datasets import load_mzml_path


pytest.importorskip("pyopenms")


def test_specread_mzml():
    filename = load_mzml_path()
    spec = specread(filename)
    assert isinstance(spec, list)
    assert all([isinstance(sp, Spectrum) for sp in spec])
    sp = spec[0]
    assert sp.amplitudes.shape == (282,)
    assert sp.wavelength.shape == (282,)
    assert sp.meta['filename'] == basename(filename)


def test_get_reader():
    filename = load_mzml_path()
    R = Request(filename)
    F = formats["MZML"]
    assert F.can_read(R)
    reader = F.get_reader(R)
    assert reader.get_length() == 531
    spec = reader.get_data(0)
    assert spec.amplitudes.shape == (282,)
    assert spec.wavelength.shape == (282,)
    assert spec.meta['filename'] == basename(filename)
    assert spec.amplitudes[0] == pytest.approx(37.384331)
