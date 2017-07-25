"""Interface plugin resource"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import os
import sys
from six import string_types, binary_type

URI_FILE = 2
URI_FILENAME = 3


class Request(object):
    """Interface between a plugin and the spectra resource.

    Represents a request for reading an spectra resource. This object wraps
    information to that request and acts as an interface for the plugins to
    several resources; it allows the user to read from filenames, files but
    offer a simple interface to the plugins via :func:`get_file` and
    :func:`specio.get_local_filename`.

    For each read operation a single Request instance is used and passed to the
    can_read method of a format, and subsequently to the Reader class. This
    allows rudimentary passing of information between different formats and
    between a format and associated reader.

    Parameters
    ----------
    uri : {str, file}
        The resource to load the image from.

    kwargs : dict
        Keywords to pass to the plugin.

    Attributes
    ----------
    filename : str
        The filename of the file to be read.

    """

    def __init__(self, uri, **kwargs):

        # General
        self._uri_type = None
        self._filename = None
        self._kwargs = kwargs

        # To handle the user-side
        self._bytes = None  # Incoming bytes

        # To handle the plugin side
        self._file = None               # To store the file instance
        self._firstbytes = None         # For easy header parsing

        # To store formats that may be able to fulfil this request
        # self._potential_formats = []

        # Parse what was given
        self._parse_uri(uri)

    def _parse_uri(self, uri):
        """ Try to figure our what we were given."""
        py3k = sys.version_info[0] == 3

        if isinstance(uri, string_types):
            # Explicit
            if uri.startswith('file://'):
                self._uri_type = URI_FILENAME
                self._filename = uri[7:]
            # Less explicit (particularly on py 2.x)
            elif py3k:
                self._uri_type = URI_FILENAME
                self._filename = uri
            else:  # pragma: no cover - our ref for coverage is py3k
                try:
                    isfile = os.path.isfile(uri)
                except Exception:
                    isfile = False  # If checking does not even work ...
                if isfile:
                    self._uri_type = URI_FILENAME
                    self._filename = uri
                elif len(uri) < 256:  # Can go wrong with veeery tiny images
                    self._uri_type = URI_FILENAME
                    self._filename = uri
                else:
                    self._uri_type = URI_FILENAME
                    self._filename = uri
        # Files
        if hasattr(uri, 'read') and hasattr(uri, 'close'):
            self._uri_type = URI_FILE
            self._filename = '<file>'
            self._file = uri

        # Expand user dir
        if self._uri_type == URI_FILENAME and self._filename.startswith('~'):
            self._filename = os.path.expanduser(self._filename)

        # Check if we could read it
        if self._uri_type is None:
            uri_r = repr(uri)
            if len(uri_r) > 60:
                uri_r = uri_r[:57] + '...'
            raise IOError("Cannot understand given URI: %s." % uri_r)

        # Make filename absolute
        if self._uri_type == URI_FILENAME:
            self._filename = os.path.abspath(self._filename)

        # Check whether file name is valid
        if self._uri_type == URI_FILENAME:
            fn = self._filename
            # Reading: check that the file exists (but is allowed a dir)
            if not os.path.exists(fn):
                raise IOError("No such file: '%s'" % fn)

    @property
    def filename(self):
        """Filename of the resource."""
        return self._filename

    @property
    def kwargs(self):
        """Keywords required to read the file."""
        return self._kwargs

    # For obtaining data

    def get_file(self):
        """Get a file object for the resource.

        Get a file object for the resource associated with this request.
        This method is not thread safe. Plugins do not need to close the file
        when done.

        This is the preferred way to read the data. But if a format cannot
        handle file-like objects, they should use ``get_local_filename()``.

        Parameters
        ----------
        None

        Returns
        -------
        file : file object
            The file object associated with the resource.

        """
        # Is there already a file?
        # Either _uri_type == URI_FILE, or we already opened the file,
        # e.g. by using firstbytes
        if self._file is not None:
            return self._file

        if self._uri_type == URI_FILENAME:
            self._file = open(self.filename, 'rb')

        return self._file

    def get_local_filename(self):
        """Get the filename of the resource.

        If the filename is an existing file on this filesystem, return
        that.

        Parameters
        ----------
        None

        Returns
        -------
        filename : str
            The filename associated with the resource.

        """

        if self._uri_type == URI_FILENAME:
            return self._filename
        elif self._uri_type == URI_FILE:
            return self._file.name

    def _finish(self):
        """For internal use (called when the context of the reader
        exits). Finishes this request. Close open files and process results.

        """
        # Close open files that we know of (and are responsible for)
        if self._file and self._uri_type != URI_FILE:
            self._file.close()
            self._file = None
        # Detach so gc can clean even if a reference of self lingers
        self._bytes = None

    @property
    def firstbytes(self):
        """The first 256 bytes of the file. These can be used to parse the
        header to determine the file-format."""
        if self._firstbytes is None:
            self._read_first_bytes()
        return self._firstbytes

    def _read_first_bytes(self, N=256):
        # Prepare
        f = self.get_file()
        try:
            i = f.tell()
        except Exception:
            i = None
        # Read
        self._firstbytes = read_n_bytes(f, N)
        # Set back
        try:
            if i is None:
                raise Exception('cannot seek with None')
            f.seek(i)
        except Exception:
            # Prevent get_file() from reusing the file
            self._file = None
            # If the given URI was a file object, we have a problem,
            if self._uri_type == URI_FILE:
                raise IOError('Cannot seek back after getting firstbytes!')


def read_n_bytes(f, N):
    """Read the N first bytes of a file object.

    Read n bytes from the given file, or less if the file has less
    bytes. Returns zero bytes if the file is closed.

    Parameters
    ----------
    f : file object
        The file object to read.

    N : int
        The number of byte to read.

    Returns
    -------
    bb : binary_type
        The N first bytes.

    """
    bb = binary_type()
    while len(bb) < N:
        extra_bytes = f.read(N-len(bb))
        if not extra_bytes:
            break
        bb += extra_bytes
    return bb
