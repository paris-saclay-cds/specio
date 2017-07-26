"""Test that SPC file is retrieved."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from specio.datasets import load_spc_path


def test_load_spc_path():
    path_data = load_spc_path()
    assert 'datasets/data/spectra.spc' in path_data
