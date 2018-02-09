"""
These functions represent specio's main interface for the user. They provide a
common API to read spectra data for a large variety of formats. All read
functions accept keyword arguments, which are passed on to the format that does
the actual work.  To see what keyword arguments are supported by a specific
format, use the :func:`.help` function.

Functions for reading:

  * :func:`.specread` - read a file with spectra from the specified uri

More control:

For a larger degree of control, specio provides a function
:func:`.get_reader`. It returns an :class:`.Reader` object, which can be used
to read data and meta data in a more controlled manner.  This also allows
specific scientific formats to be exposed in a way that best suits that
file-format.

----

Supported resource URI's:

All functions described here accept a URI to describe the resource to
read from or write to. These can be a wide range of things.

For reading:

* a normal filename, e.g. ``'c:\\foo\\bar.png'``
* a file object with a ``read()`` / ``write()`` method.

"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import print_function

import os
import glob
from itertools import chain

import numpy as np

from . import Request
from .util import Spectrum
from .. import formats


def help(name=None):
    """Print the help regarding a given format.

    Print the documentation of the format specified by name, or a list of
    supported formats if name is omitted.

    Parameters
    ----------
    name : str
        Can be the name of a format, a filename extension, or a full
        filename.

    """
    if not name:
        print(formats)
    else:
        print(formats[name])

# Base functions that return a reader


def get_reader(uri, format=None, **kwargs):
    """Return a Reader instance.

    Returns a :class:`.Reader` object which can be used to read data
    and meta data from the specified file.

    Parameters
    ----------
    uri : {str, file}
        The resource to load the image from, e.g. a filename.

    format : str
        The format to use to read the file. By default specio selects
        the appropriate for you based on the filename and its contents.

    kwargs : dict
        Further keyword arguments are passed to the reader. See :func:`.help`
        to see what arguments are available for a particular format.

    Returns
    -------
    reader : Format.Reader
        :class:`specio.Reader` instance allowing to read the data.

    """

    # Create request object
    request = Request(uri, **kwargs)

    # Get format
    if format is not None:
        format = formats[format]
    else:
        format = formats.search_read_format(request)
    if format is None:
        raise ValueError('Could not find a format to read the specified file')

    # Return its reader object
    return format.get_reader(request)

# Spectra


def _get_reader_get_data(uri, format, **kwargs):
    """Get the reader and the associated data."""
    reader = get_reader(uri, format, **kwargs)
    with reader:
        return reader.get_data(index=None)


def _validate_filenames(uri):
    """Check the filenames and expand in the case of wildcard.

    Parameters
    ----------
    uri : {str, list of str, file}
        The resource to load the spectrum from. The input accepted are:

        * a filename or a list of filename of spectrum;
        * a filename or a list of filename containing a wildcard
          (e.g. ``'./data/*.spc'``).

    Returns
    -------
    filenames : list of str
        Returns a list of all file names.

    """
    if isinstance(uri, list):
        return list(chain.from_iterable(
            [sorted(glob.glob(os.path.expanduser(f))) for f in uri]))
    else:
        return sorted(glob.glob(os.path.expanduser(uri)))


def _zip_spectrum(spectrum, tol_wavelength):
    """Compress if possible several Spectrum into a single one.

    Parameters
    ----------
    spectrum : list of Spectrum
        The list of Spectrum to zip.

    tol_wavelength : float
        Tolerance to merge spectrum when their wavelength are slightly
        different.

    Returns
    -------
    zipped_spectrum : Spectrum or list of Spectrum
        The zipped spectra(um) if it was possible to zip them.

    """
    all_spectrum = all([isinstance(sp, Spectrum) for sp in spectrum])

    if all_spectrum:
        # check that the wavelength of the different spectrum are the
        # same and concatenate all spectrum in a single data structure
        wavelength = spectrum[0].wavelength
        try:
            consistent_wavelength = [np.allclose(sp.wavelength,
                                                 wavelength,
                                                 atol=tol_wavelength)
                                     for sp in spectrum]
            if not all(consistent_wavelength):
                return spectrum

        except ValueError:
            # the above comparison will fail when two arrays have
            # different sizes
            return spectrum

        else:
            spectrum_2d, meta_2d = zip(*[(sp.amplitudes, sp.meta)
                                         for sp in spectrum])
            return Spectrum(np.vstack(spectrum_2d),
                            wavelength,
                            meta_2d)

    else:
        # chain the spectrum into a single list
        output_spectrum = []
        for sp in spectrum:
            if isinstance(sp, list):
                output_spectrum += sp
            else:
                output_spectrum.append(sp)
        return output_spectrum


def specread(uri, format=None, tol_wavelength=1e-5, **kwargs):
    """Read spectra in a given format.

    Reads spectrum from the specified file. Returns a list or a
    :class:`specio.Spectrum` instance containing the data, wavelength, and the
    meta data

    Parameters
    ----------
    uri : {str, list of str, file}
        The resource to load the spectrum from. The input accepted are:

        * a filename or a list of filename of spectrum;
        * a filename or a list of filename containing a wildcard
          (e.g. ``'./data/*.spc'``);
        * a file object.

    format : str
        The format to use to read the file. By default specio selects
        the appropriate for you based on the filename and its contents.

    tol_wavelength : float, optional
        Tolerance to merge spectrum when their wavelength are slightly
        different.

    kwargs : dict
        Further keyword arguments are passed to the reader. See :func:`.help`
        to see what arguments are available for a particular format.

    Returns
    -------
    spectrum : specio.core.Spectrum or a list of specio.core.Spectrum
        A :class:`specio.core.Spectrum` or a list of
        :class:`specio.core.Spectrum`.
        A :class:`specio.core.Spectrum` contains:

        * a 1D ndarray of shape (n_wavelength,) or 2D ndarray of shape
          (n_spectra, n_wavelength) ``amplitudes``;
        * a 1D ndarray of shape (n_wavelength,) ``wavelength``;
        * a dict ``meta``.

    """
    filenames = _validate_filenames(uri)
    spectrum = [_get_reader_get_data(f, format, **kwargs)
                for f in filenames]
    return (_zip_spectrum(spectrum, tol_wavelength) if len(spectrum) > 1
            else spectrum[0])
