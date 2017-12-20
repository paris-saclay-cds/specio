"""Test that SPC file is retrieved."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from specio.datasets import load_sp_path


def test_load_sp_path():
    path_data = load_sp_path()
    assert 'datasets/data/spectra.sp' in path_data
