"""Test that all spectra files are retrieved."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import pytest

from specio.datasets import load_fsm_path
from specio.datasets import load_sp_path
from specio.datasets import load_spc_path


@pytest.mark.parametrize(
    "path_data,extension",
    [(load_fsm_path(), 'fsm'),
     (load_sp_path(), 'sp'),
     (load_spc_path(), 'spc')])
def test_load_spectra_path(path_data, extension):
    assert 'datasets/data/spectra.' + extension in path_data
