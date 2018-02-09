"""Common tests using the toy data."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import sys
from os.path import basename

import pytest

from specio import specread
from specio import formats
from specio.core import Request
from specio.core import Spectrum
from specio.datasets import load_csv_path
from specio.datasets import load_fsm_path
from specio.datasets import load_spc_path
from specio.datasets import load_sp_path
from specio.datasets import load_mzml_path


def skip_windows_py27():
    return pytest.mark.skipif(
        (sys.platform == 'win32') and (sys.version_info < (3, 5)),
        reason="OpenMS not available")


def _check_spectra(spec, filename, filename_cmp, spectrum_shape,
                   wavelength_shape):
    assert spec.amplitudes.shape == spectrum_shape
    assert spec.wavelength.shape == wavelength_shape
    if isinstance(spec.meta, tuple):
        for m in spec.meta:
            if filename_cmp:
                assert m['filename'] == basename(filename)
            else:
                assert m['filename']
    else:
        if filename_cmp:
            assert spec.meta['filename'] == basename(filename)
        else:
            assert spec.meta['filename']


@pytest.mark.parametrize(
    "filename,filename_cmp,spectrum_shape,wavelength_shape",
    [(load_fsm_path(), True, (7998, 1641), (1641,)),
     (load_spc_path(), True, (1911,), (1911,)),
     (load_sp_path(), True, (3301,), (3301,)),
     pytest.param(load_mzml_path(), True, (282,), (282,),
                  marks=skip_windows_py27()),
     (load_csv_path(), False, (84, 1732,), (1732,))])
def test_specread(filename, filename_cmp, spectrum_shape, wavelength_shape):
    spec = specread(filename)
    if isinstance(spec, Spectrum):
        _check_spectra(spec, filename, filename_cmp, spectrum_shape,
                       wavelength_shape)
    elif isinstance(spec, list):
        assert all([isinstance(sp, Spectrum) for sp in spec])
        sp = spec[0]
        _check_spectra(sp, filename, filename_cmp, spectrum_shape,
                       wavelength_shape)
    else:
        raise AssertionError('specread should return either a Spectrum '
                             'instance or a list of Spectrum. '
                             'Got {!r}.'.format(spec))


def _check_get_spectra(spec, filename, filename_cmp, spectrum_shape,
                       wavelength_shape):
    assert spec.amplitudes.shape == spectrum_shape
    assert spec.wavelength.shape == wavelength_shape
    if isinstance(spec.meta, tuple):
        for m in spec.meta:
            if filename_cmp:
                assert m['filename'] == basename(filename)
            else:
                assert m['filename']
    else:
        if filename_cmp:
            assert spec.meta['filename'] == basename(filename)
        else:
            assert spec.meta['filename']


@pytest.mark.parametrize(
    "filename,filename_cmp,format_spec,len_spectrum,spectrum_shape,"
    "wavelength_shape,first_value",
    [(load_fsm_path(), True, "FSM", 7998, (7998, 1641), (1641,), 38.656551),
     (load_spc_path(), True, "SPC", 1, (1911,), (1911,), 1487.0),
     (load_sp_path(), True, "SP", 1, (3301,), (3301,), 0.03723936007346753),
     pytest.param(
         load_mzml_path(), True, "MZML", 531, (282,), (282,), 37.384331,
         marks=skip_windows_py27()),
     (load_csv_path(), False, "CSV", 84, (84, 1732), (1732, ), 173.333343505)])
def test_get_reader(filename, filename_cmp, format_spec, len_spectrum,
                    spectrum_shape, wavelength_shape, first_value):
    R = Request(filename)
    F = formats[format_spec]
    assert F.can_read(R)
    reader = F.get_reader(R)
    assert reader.get_length() == len_spectrum
    spec = reader.get_data()
    if isinstance(spec, Spectrum):
        _check_get_spectra(spec, filename, filename_cmp, spectrum_shape,
                           wavelength_shape)
    spec = reader.get_data(0)
    assert spec.amplitudes.size == spectrum_shape[-1]
    assert spec.wavelength.size == wavelength_shape[-1]
    assert spec.amplitudes[0] == pytest.approx(first_value)
