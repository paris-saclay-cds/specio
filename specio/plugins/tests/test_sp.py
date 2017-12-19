"""Test the SP plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join

from specio import specread

DATA_PATH = dirname(__file__)


def test_sp_specread():
    filename = join(DATA_PATH, 'data', 'spectra.sp')
    X = specread(filename)
