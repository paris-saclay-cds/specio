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

from . import Request
from .. import formats


def help(name=None):
    """Print the help regarding a given format.

    Print the documentation of the format specified by name, or a list of
    supported formats if name is omitted.

    Parameters
    ----------
    name : str
        Can be the name of a format, a filename extension, or a full
        filename. See also the :doc:`formats page <formats>`.

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


def specread(uri, format=None, **kwargs):
    """Read spectra in a given format.

    Reads spectrum from the specified file. Returns a :class:`specio.Spectrum`
    instance containing the data, wavelength, and the meta data

    Parameters
    ----------
    uri : {str, file}
        The resource to load the spectrum from, e.g. a filename or file object,
        see the docs for more info.

    format : str
        The format to use to read the file. By default specio selects
        the appropriate for you based on the filename and its contents.

    kwargs : dict
        Further keyword arguments are passed to the reader. See :func:`.help`
        to see what arguments are available for a particular format.

    Returns
    -------
    spectrum : specio.Spectrum
        A :class:`specio.Spectrum` instance containing the data, wavelength,
        and meta data.

    """

    # Get reader and read first
    reader = read(uri, format, **kwargs)
    with reader:
        return reader.get_data(index=None)

# Aliases


read = get_reader
