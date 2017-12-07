"""Example plugin. You can use this as a template for your own plugin."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

import numpy as np

from .. import formats
from ..core import Format
from ..core import Spectrum


class DummyFormat(Format):
    """ The dummy format is an example format that does nothing.
    It will never indicate that it can read a file. When
    explicitly asked to read, it will simply read the bytes.

    This documentation is shown when the user does ``help('thisformat')``.

    Parameters
    ----------
    Specify arguments in numpy doc style here.

    Attributes
    ----------
    Specify the specific attributes that can be useful.

    """

    def _can_read(self, request):
        # This method is called when the format manager is searching
        # for a format to read a certain image. Return True if this format
        # can do it.
        #
        # The format manager is aware of the extensions
        # that each format can handle. It will first ask all formats
        # that *seem* to be able to read it whether they can. If none
        # can, it will ask the remaining formats if they can: the
        # extension might be missing, and this allows formats to provide
        # functionality for certain extensions, while giving preference
        # to other plugins.
        #
        # If a format says it can, it should live up to it. The format
        # would ideally check the request.firstbytes and look for a
        # header of some kind.
        #
        # The request object has:
        # request.filename: a representation of the source (only for reporting)
        # request.firstbytes: the first 256 bytes of the file.

        if request.filename.lower().endswith(self.extensions):
            return True
        return False
    # -- reader

    class Reader(Format.Reader):

        def _open(self, some_option=False, length=1):
            # Specify kwargs here. Optionally, the user-specified kwargs
            # can also be accessed via the request.kwargs object.
            #
            # The request object provides two ways to get access to the
            # data. Use just one:
            #  - Use request.get_file() for a file object (preferred)
            #  - Use request.get_local_filename() for a file on the system
            self._fp = self.request.get_file()
            self._length = length  # passed as an arg in this case for testing
            self._data = None

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass

        def _get_length(self):
            # Return the number of images. Can be np.inf
            return self._length

        def _get_data(self, index=None):
            # Return the data and meta data for the given index
            if index is not None and index >= self._length:
                raise IndexError('Image index %i > %i' % (index, self._length))
            # Read all bytes
            if self._data is None:
                self._data = self._fp.read()
            # Put in a numpy array
            spec = np.frombuffer(self._data, 'uint8')
            spec = spec[np.newaxis, :]
            # Return array and dummy meta data
            return Spectrum(spec, np.squeeze(spec), {})

        def _get_meta_data(self, index):
            # Get the meta data for the given index. If index is None, it
            # should return the global meta data.
            return {}  # This format does not support meta data


# Register. You register an *instance* of a Format class. Here specify:
format = DummyFormat('dummy',  # short name
                     'An example format that does nothing.',  # one line descr.
                     '.foobar .nonexistentext',  # list of extensions
                     )
formats.add_format(format)
