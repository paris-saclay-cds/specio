"""Exceptions utilities."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause


class CannotReadSpectraError(RuntimeError):
    """Exception to be used by plugins to indicate that a spectra could not be
    read, even though it should be a valid index.
    """
    pass
