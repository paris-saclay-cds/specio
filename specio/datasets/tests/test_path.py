"""Test that all spectra files are retrieved."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import join

import pytest

from specio.datasets import load_fsm_path
from specio.datasets import load_mzml_path
from specio.datasets import load_sp_path
from specio.datasets import load_spc_path
from specio.datasets import load_csv_path


@pytest.mark.parametrize(
    "path_data,extension",
    [(load_fsm_path(), 'fsm'),
     (load_mzml_path(), 'mzml'),
     (load_sp_path(), 'sp'),
     (load_spc_path(), 'spc'),
     (load_csv_path(), 'csv')])
def test_load_spectra_path(path_data, extension):
    assert join('datasets', 'data', 'spectra.' + extension) in path_data
