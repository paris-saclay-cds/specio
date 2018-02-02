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
from pandas.testing import assert_frame_equal

from specio import specread
from specio.datasets import load_spc_path
from specio.core.util import Spectrum, Dict


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


def test_spectrum_to_dataframe():
    spec = specread(load_spc_path())
    df_spec = spec.to_dataframe()
    assert_array_equal(df_spec.index.values, np.array(spec.meta['filename']))
    assert_allclose(df_spec.columns.values, spec.wavelength)
    assert_allclose(df_spec.values, np.atleast_2d(spec.amplitudes))


def test_spectrum_to_csv():
    spec = specread(load_spc_path())
    tmp_dir = mkdtemp()
    filename = os.path.join(tmp_dir, 'spectra.csv')

    try:
        spec.to_csv(filename)
        df = pd.read_csv(filename, index_col=0)
        df.columns = df.columns.astype(float)
        assert_frame_equal(df, spec.to_dataframe(),
                           check_exact=False,
                           check_less_precise=True)
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
