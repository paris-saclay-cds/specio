"""Common tests using the toy data."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import basename

import pytest

from specio import specread
from specio import formats
from specio.core import Request
from specio.core import Spectrum
from specio.datasets import load_fsm_path
from specio.datasets import load_spc_path
from specio.datasets import load_sp_path
from specio.datasets import load_mzml_path


@pytest.mark.parametrize(
    "filename,spectrum_shape,wavelength_shape",
    [(load_fsm_path(), (7998, 1641), (1641,)),
     (load_mzml_path(), (531,), (531,)),
     (load_spc_path(), (1911,), (1911,)),
     (load_sp_path(), (3301,), (3301,))])
def test_specread(filename, spectrum_shape, wavelength_shape):
    spec = specread(filename)
    assert isinstance(spec, Spectrum)
    assert spec.amplitudes.shape == spectrum_shape
    assert spec.wavelength.shape == wavelength_shape
    assert spec.meta['filename'] == basename(filename)


@pytest.mark.parametrize(
    "filename,format_spec,spectrum_shape,wavelength_shape,first_value",
    [(load_fsm_path(), "FSM", (7998, 1641), (1641,), 38.656551),
     (load_mzml_path(), "MZML", (531,), (531,), None),
     (load_spc_path(), "SPC", (1911,), (1911,), 1487.0),
     (load_sp_path(), "SP", (3301,), (3301,), 0.03723936007346753)])
def test_get_reader(filename, format_spec, spectrum_shape, wavelength_shape,
                    first_value):
    R = Request(filename)
    F = formats[format_spec]
    assert F.can_read(R)
    reader = F.get_reader(R)
    if len(spectrum_shape) == 1:
        assert reader.get_length() == 1
    else:
        assert reader.get_length() == spectrum_shape[0]
    spec = reader.get_data()
    assert reader.get_meta_data()['filename'] == basename(filename)
    assert spec.amplitudes.shape == spectrum_shape
    assert spec.wavelength.shape == wavelength_shape
    spec = reader.get_data(0)
    assert spec.amplitudes.size == spectrum_shape[-1]
    assert spec.wavelength.size == wavelength_shape[-1]
    assert spec.amplitudes[0] == pytest.approx(first_value)
