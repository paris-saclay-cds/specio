"""Retrieve the path of the SPC toy spectra."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join


def load_spc_path():
    """Return the path to the SPC toy file.

    Parameters
    ----------
    None

    Returns
    -------
    path_data : str
        The path to the SPC data.

    Examples
    --------
    >>> from specio.datasets import load_spc_path
    >>> load_spc_path() # doctest: +ELLIPSIS
    '...spectra.spc'

    """
    module_path = dirname(__file__)
    return join(module_path, 'data', 'spectra.spc')
