"""Test that FSM file is retrieved."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from specio.datasets import load_fsm_path


def test_load_fsm_path():
    path_data = load_fsm_path()
    assert 'datasets/data/spectra.fsm' in path_data
