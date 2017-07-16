"""Test util classes"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import numpy as np
from numpy.testing import assert_allclose

from specio.core.util import Spectrum, Dict
from specio.testing import assert_raises_regex

RELATIVE_TOLERANCE = 1e-4


def test_spectrum_error():
    assert_raises_regex(ValueError, "expects spectrum to be a numpy array",
                        Spectrum, 0, np.zeros((100,)))
    assert_raises_regex(ValueError, "expects wavelength to be a numpy array",
                        Spectrum, np.random.random((100, 100)), 0)
    assert_raises_regex(ValueError, "expects meta data to be a dict",
                        Spectrum, np.random.random((100, 100)),
                        np.random.random(100,), 0)
    assert_raises_regex(ValueError, "2-dimensional",
                        Spectrum, np.random.random((100, 100, 100)),
                        np.random.random(100,))
    assert_raises_regex(ValueError, "1-dimensional",
                        Spectrum, np.random.random((100, 100)),
                        np.random.random((100, 100)))
    assert_raises_regex(ValueError, "The number of wavelength in",
                        Spectrum, np.random.random((100, 1000)),
                        np.random.random((100,)))


def test_spectrum():
    rng = np.random.RandomState(0)
    spec = Spectrum(rng.random_sample((1, 10)), rng.random_sample(10),
                    {'kind': 'random'})

    spectrum_expected = np.array([[0.548814, 0.715189, 0.602763, 0.544883,
                                   0.423655, 0.645894, 0.437587, 0.891773,
                                   0.963663,  0.383442]])
    wavelength_expected = np.array([0.791725, 0.528895, 0.568045, 0.925597,
                                    0.071036, 0.087129, 0.020218, 0.83262,
                                    0.778157,  0.870012])

    assert_allclose(spec._spectrum, spectrum_expected,
                    rtol=RELATIVE_TOLERANCE)
    assert_allclose(spec._wavelength, wavelength_expected,
                    rtol=RELATIVE_TOLERANCE)
    assert spec._meta == {'kind': 'random'}


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
    assert_raises_regex(AttributeError, "Reserved name, this key can only"
                        " be set via", D.__setattr__, 'copy', False)
    assert_raises_regex(AttributeError, "'Dict' object has no attribute"
                        " 'notinD'", D.__getattribute__, 'notinD')
