"""Test util classes"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import os
from tempfile import mkdtemp
from shutil import rmtree

import pytest

import numpy as np
import pandas as pd

from numpy.testing import assert_allclose
from numpy.testing import assert_array_equal

from specio import specread
from specio.datasets import load_spc_path
from specio.core.util import Spectrum, Dict


module_path = os.path.dirname(__file__)


@pytest.mark.parametrize(
    "spectrum,wavelength,msg",
    [(np.ones((100, 100, 100)), np.ones((10,)), "1-D or 2-D"),
     (np.ones((100, 100)), np.ones((100, 100)), "1-D or 2-D"),
     (np.ones((100, 1000)), np.ones((100,)), "The number of frequencies"),
     (np.ones((10,)), np.ones((100,)), "The number of frequencies")])
def test_spectrum_error(spectrum, wavelength, msg):
    with pytest.raises(ValueError, message=msg):
        Spectrum(spectrum, wavelength)


@pytest.mark.parametrize(
    "spectrum,wavelength,metadata",
    [(np.ones((1, 10)), np.ones((10,)), {'kind': 'random'}),
     (np.ones((10,)), np.ones((10,)), {'kind': 'random'})])
def test_spectrum(spectrum, wavelength, metadata):
    spec = Spectrum(spectrum, wavelength, metadata)
    assert_allclose(spec.amplitudes, spectrum)
    assert_allclose(spec.wavelength, wavelength)
    assert spec.meta == {'kind': 'random'}


@pytest.mark.parametrize(
    "filename",
    [(os.path.join(module_path, 'data', '*.spc')),
     (load_spc_path())])
def test_spectrum_to_dataframe(filename):
    spec = specread(filename)
    df_spec = spec.to_dataframe()
    if isinstance(spec.meta, tuple):
        expected_index = np.array([meta['filename'] for meta in spec.meta])
    else:
        expected_index = np.array(spec.meta['filename'])
    assert_array_equal(df_spec.index.values, expected_index)
    assert_allclose(df_spec.columns.values, spec.wavelength)
    assert_allclose(df_spec.values, np.atleast_2d(spec.amplitudes))


@pytest.mark.parametrize(
    "filename",
    [(os.path.join(module_path, 'data', '*.spc')),
     (load_spc_path())])
def test_spectrum_to_csv(filename):
    spec = specread(filename)
    tmp_dir = mkdtemp()
    filename = os.path.join(tmp_dir, 'spectra.csv')

    try:
        spec.to_csv(filename)
        df = pd.read_csv(filename, index_col=0)
        df.columns = df.columns.astype(float)
        assert_allclose(df.values, spec.to_dataframe().values)
        assert_allclose(df.columns.values, spec.to_dataframe().columns.values)
        assert_array_equal(df.index.values, spec.to_dataframe().index.values)
    finally:
        rmtree(tmp_dir)


def test_util_dict():
    # Dict class
    D = Dict()
    D['foo'] = 1
    D['bar'] = 2
    D['spam'] = 3
    assert list(D.values()) == [1, 2, 3]
    #
    assert D.spam == 3
    D.spam = 4
    assert D['spam'] == 4
    # Can still use copy etc.
    assert D.copy() == D
    assert 'spam' in D.keys()
    # Can also insert non-identifiers
    D[3] = 'not an identifier'
    D['34a'] = 'not an identifier'
    D[None] = 'not an identifier'
    # dir
    names = dir(D)
    assert 'foo' in names
    assert 'spam' in names
    assert 3 not in names
    assert '34a' not in names
    # Fail
    with pytest.raises(AttributeError):
        D.__setattr__('copy', False)
    with pytest.raises(AttributeError):
        D.__getattribute__('notinD')
