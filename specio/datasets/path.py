"""Retrieve all paths for the different toy spectra"""

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


def load_csv_path():
    """Return the path to the CSV toy file.

    Parameters
    ----------
    None

    Returns
    -------
    path_data : str
        The path to the CSV data.

    Examples
    --------
    >>> from specio.datasets import load_csv_path
    >>> load_csv_path() # doctest: +ELLIPSIS
    '...spectra.csv'

    """
    module_path = dirname(__file__)
    return join(module_path, 'data', 'spectra.csv')
