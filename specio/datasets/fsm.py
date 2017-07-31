"""Retrieve the path of the FSM toy spectra."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join


def load_fsm_path():
    """Return the path to the FSM toy file.

    Parameters
    ----------
    None

    Returns
    -------
    path_data : str
        The path to the FSM data.

    Examples
    --------
    >>> from specio.datasets import load_fsm_path
    >>> load_fsm_path() # doctest: +ELLIPSIS
    '...spectra.fsm'

    """
    module_path = dirname(__file__)
    return join(module_path, 'data', 'spectra.fsm')
