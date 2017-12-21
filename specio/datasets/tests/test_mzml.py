"""Test that mzML file is retrieved."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from specio.datasets import load_mzml_path


def test_load_mzml_path():
    path_data = load_mzml_path()
    assert 'datasets/data/spectra.mzml' in path_data
