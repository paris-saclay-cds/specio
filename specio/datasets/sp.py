"""Retrieve the path of the SP toy spectra."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join


def load_sp_path():
    """Return the path to the SP toy file.

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
    >>> load_sp_path() # doctest: +ELLIPSIS
    '...spectra.sp'

    """
    module_path = dirname(__file__)
    return join(module_path, 'data', 'spectra.sp')
