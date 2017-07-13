from __future__ import print_function

from .. import Request
from .. import formats


def help(name=None):
    """ help(name=None)

    Print the documentation of the format specified by name, or a list
    of supported formats if name is omitted.

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


def get_reader(uri, format=None, mode='?', **kwargs):
    """ get_reader(uri, format=None, mode='?', **kwargs)

    Returns a :class:`.Reader` object which can be used to read data
    and meta data from the specified file.

    Parameters
    ----------
    uri : {str, file}
        The resource to load the image from, e.g. a filename.

    format : str
        The format to use to read the file. By default specio selects
        the appropriate for you based on the filename and its contents.

    mode : {'s', 'S', '?'}
        Used to give the reader a hint on what the user expects (default "?"):
        "s" for a single spectra, "S" for multiple spectrum or
        "?" for don't care.

    kwargs : ...
        Further keyword arguments are passed to the reader. See :func:`.help`
        to see what arguments are available for a particular format.
    """

    # Create request object
    request = Request(uri, mode, **kwargs)

    # Get format
    if format is not None:
        format = formats[format]
    else:
        format = formats.search_read_format(request)
    if format is None:
        raise ValueError('Could not find a format to read the specified file '
                         'in mode %r' % mode)

    # Return its reader object
    return format.get_reader(request)

# Images


def imread(uri, format=None, **kwargs):
    """ imread(uri, format=None, **kwargs)

    Reads an image from the specified file. Returns a numpy array, which
    comes with a dict of meta data at its 'meta' attribute.

    Note that the image data is returned as-is, and may not always have
    a dtype of uint8 (and thus may differ from what e.g. PIL returns).

    Parameters
    ----------
    uri : {str, file}
        The resource to load the image from, e.g. a filename, http address or
        file object, see the docs for more info.
    format : str
        The format to use to read the file. By default imageio selects
        the appropriate for you based on the filename and its contents.
    kwargs : ...
        Further keyword arguments are passed to the reader. See :func:`.help`
        to see what arguments are available for a particular format.
    """

    # Get reader and read first
    reader = read(uri, format, 'i', **kwargs)
    with reader:
        return reader.get_data(0)

# Aliases


read = get_reader
