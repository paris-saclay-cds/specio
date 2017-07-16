"""Test the testing"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from specio.testing import assert_raises_regex


def raise_error(arg1, arg2, arg3=None):
    raise ValueError("Raise an error.")


def test_assert_raises_regex():
    assert_raises_regex(ValueError, "Raise an error.", raise_error, 0, 1,
                        arg3=2)
