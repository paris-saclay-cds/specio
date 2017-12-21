"""Retrieve the path of the mzML toy spectra."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from os.path import dirname, join


def load_mzml_path():
    """Return the path to the mzML toy file.

    Parameters
    ----------
    None

    Returns
    -------
    path_data : str
        The path to the mzML data.

    Examples
    --------
    >>> from specio.datasets import load_mzml_path
    >>> load_mzml_path() # doctest: +ELLIPSIS
    '...spectra.mzml'

    """
    module_path = dirname(__file__)
    return join(module_path, 'data', 'spectra.mzml')
