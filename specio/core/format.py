"""Base class used by the plugin to read a specific format."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import print_function

import os
from warnings import warn
from six import string_types

from .exceptions import CannotReadSpectraError
from .util import Spectrum


class Format(object):
    """Represents an implementation to read a particular spectrum format.

    A format instance is responsible for: (i) providing information about a
    format, (ii) determining whether a certain file can be read with this
    format, and (iii) providing a reader class.

    Generally, ``specio`` will select the right format and use that to read the
    spectrum. A format can also be explicitly chosen in all read function. Use
    ``print(format)`` or ``help(format)`` to see its documentation.

    To implement a specific format, one should create a subclass of ``Format``
    and the ``Format.Reader class.

    Parameters
    ----------
    name : str
        A short name of this format. Users can select a format using its name.

    description : str
        A one-line description of the format.

    extensions : str | list | None
        List of filename extensions that this format supports. If a
        string is passed it should be space or comma separated. The
        extensions are used in the documentation and to allow users to
        select a format by file extension. It is not used to determine
        what format to use for reading a file.

    modes : str
        A string containing the modes that this format can handle ('sS'),
        's' for a single spectrum, 'S' for multiple spectrum.
        This attribute is used in the documentation and to select the
        formats when reading a file.
    """

    def __init__(self, name, description, extensions=None, modes=None):
        self._name = name.upper()
        self._description = description

        # Store extensions, do some effort to normalize them.
        # They are stored as a list of lowercase strings without leading dots.
        if extensions is None:
            extensions = []
        elif isinstance(extensions, string_types):
            extensions = extensions.replace(',', ' ').split(' ')

        if isinstance(extensions, (tuple, list)):
            self._extensions = tuple(['.' + e.strip('.').lower()
                                      for e in extensions if e])
        else:
            raise ValueError('Invalid value for extensions given.')

        # Store mode
        self._modes = modes or ''
        if not isinstance(self._modes, string_types):
            raise ValueError('Invalid value for modes given.')
        for m in self._modes:
            if m not in 'sS?':
                raise ValueError('Invalid value for mode given.')

    def __repr__(self):
        # Short description
        return '<Format %s - %s>' % (self.name, self.description)

    def __str__(self):
        return self.doc

    @property
    def doc(self):
        """The documentation for this format (name + description + docstring).
        """
        # Our docsring is assumed to be indented by four spaces. The
        # first line needs special attention.
        return '%s - %s\n\n    %s\n' % (self.name, self.description,
                                        self.__doc__.strip())

    @property
    def name(self):
        """ The name of this format.
        """
        return self._name

    @property
    def description(self):
        """A short description of this format.
        """
        return self._description

    @property
    def extensions(self):
        """A list of file extensions supported by this plugin.
        These are all lowercase with a leading dot.
        """
        return self._extensions

    @property
    def modes(self):
        """A string specifying the modes that this format can handle.
        """
        return self._modes

    def get_reader(self, request):
        """get_reader(request)

        Return a reader object that can be used to read data and info
        from the given file. Users are encouraged to use specio.get_reader()
        instead.
        """
        select_mode = request.mode if request.mode in 'sS' else ''
        if select_mode not in self.modes:
            raise RuntimeError('Format %s cannot read in mode %r' %
                               (self.name, select_mode))
        return self.Reader(self, request)

    def can_read(self, request):
        """ can_read(request)

        Get whether this format can read data from the specified uri.
        """
        return self._can_read(request)

    def _can_read(self, request):
        """Implemented by the plugins."""
        return None

    class Reader(object):
        """
        The purpose of a reader object is to read data from an image
        resource, and should be obtained by calling :func:`.get_reader`.

        A reader can be used as an iterator to read multiple images,
        and (if the format permits) only reads data from the file when
        new data is requested (i.e. streaming). A reader can also be
        used as a context manager so that it is automatically closed.

        Plugins implement Reader's for different formats. Though rare,
        plugins may provide additional functionality (beyond what is
        provided by the base reader class).
        """

        def __init__(self, format, request):
            self.__closed = False
            self._BaseReader_last_index = -1
            self._format = format
            self._request = request
            # Open the reader/writer
            self._open(**self.request.kwargs.copy())

        @property
        def format(self):
            """ The :class:`.Format` object corresponding to the current
            read/write operation.
            """
            return self._format

        @property
        def request(self):
            """ The :class:`.Request` object corresponding to the
            current read operation.
            """
            return self._request

        def get_length(self):
            """ get_length()

            Get the number of spectrum in the file. (Note: you can also
            use ``len(reader_object)``.)

            The result can be:

                * 0 for files that only have meta data
                * 1 for singleton spectrum
                * N for spectra series
            """
            return self._get_length()

        def get_data(self, index, **kwargs):
            """ get_data(index, **kwargs)

            Read data from the file, using the spectrum index. The
            returned spectrum has a 'meta' attribute with the meta data.

            Some formats may support additional keyword arguments. These are
            listed in the documentation of those formats.
            """
            self._checkClosed()
            self._BaseReader_last_index = index
            spectrum, wavelength, meta = self._get_data(index, **kwargs)
            return Spectrum(spectrum, wavelength, meta)

        def get_next_data(self, **kwargs):
            """ get_next_data(**kwargs)

            Read the next spectra from the series.

            Some formats may support additional keyword arguments. These are
            listed in the documentation of those formats.
            """
            return self.get_data(self._BaseReader_last_index + 1, **kwargs)

        def get_meta_data(self, index=None):
            """ get_meta_data(index=None)

            Read meta data from the file. using the spectrum index. If the
            index is omitted or None, return the file's (global) meta data.

            Note that ``get_data`` also provides the meta data for the returned
            spectra as an atrribute of that spectra.

            The meta data is a dict, which shape depends on the format.
            """
            self._checkClosed()
            meta = self._get_meta_data(index)
            if not isinstance(meta, dict):
                raise ValueError('Meta data must be a dict, not %r' %
                                 meta.__class__.__name__)
            return meta

        def iter_data(self):
            """ iter_data()

            Iterate over all spectrum in the series. (Note: you can also
            iterate over the reader object.)

            """
            self._checkClosed()
            i, n = 0, self.get_length()
            while i < n:
                try:
                    spectrum, wavelength, meta = self._get_data(i)
                except (IndexError, CannotReadSpectraError):
                    if n - i == 1:
                        uri = self.request.filename
                        warn('Could not read last frame of %s.' % uri)
                        return
                    raise
                yield Spectrum(spectrum, wavelength, meta)
                i += 1

        # Compatibility

        def __iter__(self):
            return self.iter_data()

        def __len__(self):
            return self.get_length()

        def __enter__(self):
            self._checkClosed()
            return self

        def __exit__(self, type, value, traceback):
            if value is None:
                # Otherwise error in close hide the real error.
                self.close()

        def __del__(self):
            try:
                self.close()
            except Exception:
                pass  # Remove noise when called during interpreter shutdown

        def close(self):
            """ Flush and close the reader.
            This method has no effect if it is already closed.
            """
            if self.__closed:
                return
            self.__closed = True
            self._close()
            # Process results and clean request object
            self.request._finish()

        @property
        def closed(self):
            """ Whether the reader is closed.
            """
            return self.__closed

        def _checkClosed(self, msg=None):
            """Internal: raise an ValueError if reader is closed
            """
            if self.closed:
                what = self.__class__.__name__
                msg = msg or ("I/O operation on closed %s." % what)
                raise RuntimeError(msg)

        # To implement

        def _open(self, **kwargs):
            """ _open(**kwargs)

            Plugins should probably implement this.

            It is called when reader is created. Here the
            plugin can do its initialization. The given keyword arguments
            are those that were given by the user at specio.read().
            """
            raise NotImplementedError()

        def _close(self):
            """ _close()

            Plugins should probably implement this.

            It is called when the reader is closed. Here the plugin
            can do a cleanup, flush, etc.

            """
            raise NotImplementedError()

        def _get_length(self):
            """ _get_length()

            Plugins must implement this.

            The retured scalar specifies the number of spectra in the series.
            See Reader.get_length for more information.
            """
            raise NotImplementedError()

        def _get_data(self, index):
            """ _get_data()

            Plugins must implement this, but may raise an IndexError in
            case the plugin does not support random access.

            It should return the spectra and meta data: (ndarray, dict).
            """
            raise NotImplementedError()

        def _get_meta_data(self, index):
            """ _get_meta_data(index)

            Plugins must implement this.

            It should return the meta data as a dict, corresponding to the
            given index, or to the file's (global) meta data if index is
            None.
            """
            raise NotImplementedError()


class FormatManager(object):
    """
    There is exactly one FormatManager object in specio: ``specio.formats``.
    Its purpose it to keep track of the registered formats.

    The format manager supports getting a format object using indexing (by
    format name or extension). When used as an iterator, this object
    yields all registered format objects.

    See also :func:`.help`.
    """

    def __init__(self):
        self._formats = []
        self._formats_sorted = []

    def __repr__(self):
        return '<specio.FormatManager with %i registered formats>' % len(self)

    def __iter__(self):
        return iter(self._formats_sorted)

    def __len__(self):
        return len(self._formats)

    def __str__(self):
        ss = []
        for format in self:
            ext = ', '.join(format.extensions)
            s = '%s - %s [%s]' % (format.name, format.description, ext)
            ss.append(s)
        return '\n'.join(ss)

    def __getitem__(self, name):
        # Check
        if not isinstance(name, string_types):
            raise ValueError('Looking up a format should be done by name '
                             'or by extension.')
        if not name:
            raise ValueError('No format matches the empty string.')

        # Test if name is existing file
        if os.path.isfile(name):
            from . import Request
            format = self.search_read_format(Request(name, 'r?'))
            if format is not None:
                return format

        if '.' in name:
            # Look for extension
            e1, e2 = os.path.splitext(name.lower())
            name = e2 or e1
            # Search for format that supports this extension
            for format in self:
                if name in format.extensions:
                    return format
        else:
            # Look for name
            name = name.upper()
            for format in self:
                if name == format.name:
                    return format
            for format in self:
                if name == format.name.rsplit('-', 1)[0]:
                    return format
            else:
                # Maybe the user meant to specify an extension
                return self['.' + name.lower()]

        # Nothing found ...
        raise IndexError('No format known by name %s.' % name)

    def _sorter(val, name):
        return - ((val.name == name) + (val.name.endswith(name)))

    def sort(self, *names):
        """ sort(name1, name2, name3, ...)

        Sort the formats based on zero or more given names; a format with
        a name that matches one of the given names will take precedence
        over other formats. A match means an equal name, or ending with
        that name (though the former counts higher). Case insensitive.

        Be aware that using the function can affect the behavior of
        other code that makes use of imageio.

        Also see the ``SPECIO_FORMAT_ORDER`` environment variable.
        """
        # Check and sanitize imput
        for name in names:
            if not isinstance(name, string_types):
                raise TypeError('formats.sort() accepts only string names.')
            if any(c in name for c in '.,'):
                raise ValueError('Names given to formats.sort() should not '
                                 'contain dots or commas.')
        names = [name.strip().upper() for name in names]
        # Reset
        self._formats_sorted = list(self._formats)
        # Sort
        for name in reversed(names):
            self._formats_sorted.sort(
                key=lambda f: - ((f.name == name) + (f.name.endswith(name))))

    def add_format(self, format, overwrite=False):
        """ add_format(format, overwrite=False)

        Register a format, so that imageio can use it. If a format with the
        same name already exists, an error is raised, unless overwrite is True,
        in which case the current format is replaced.
        """
        if not isinstance(format, Format):
            raise ValueError('add_format needs argument to be a Format object')
        elif format in self._formats:
            raise ValueError('Given Format instance is already registered')
        elif format.name in self.get_format_names():
            if overwrite:
                old_format = self[format.name]
                self._formats.remove(old_format)
                if old_format in self._formats_sorted:
                    self._formats_sorted.remove(old_format)
            else:
                raise ValueError('A Format named %r is already registered, use'
                                 ' overwrite=True to replace.' % format.name)
        self._formats.append(format)
        self._formats_sorted.append(format)

    def search_read_format(self, request):
        """ search_read_format(request)

        Search a format that can read a file according to the given request.
        Returns None if no appropriate format was found. (used internally)
        """
        select_mode = request.mode if request.mode in 'sS' else ''
        select_ext = request.filename.lower()

        # Select formats that seem to be able to read it
        selected_formats = []
        for format in self:
            if select_mode in format.modes:
                if select_ext.endswith(format.extensions):
                    selected_formats.append(format)

        # Select the first that can
        for format in selected_formats:
            if format.can_read(request):
                return format

        # If no format could read it, it could be that file has no or
        # the wrong extension. We ask all formats again.
        for format in self:
            if format not in selected_formats:
                if format.can_read(request):
                    return format

    def search_write_format(self, request):
        """ search_write_format(request)

        Search a format that can write a file according to the given request.
        Returns None if no appropriate format was found. (used internally)
        """
        select_mode = request.mode if request.mode in 'sS' else ''
        select_ext = request.filename.lower()

        # Select formats that seem to be able to write it
        selected_formats = []
        for format in self:
            if select_mode in format.modes:
                if select_ext.endswith(format.extensions):
                    selected_formats.append(format)

        # Select the first that can
        for format in selected_formats:
            if format.can_write(request):
                return format

        # If none of the selected formats could write it, maybe another
        # format can still write it. It might prefer a different mode,
        # or be able to handle more formats than it says by its extensions.
        for format in self:
            if format not in selected_formats:
                if format.can_write(request):
                    return format

    def get_format_names(self):
        """ Get the names of all registered formats.
        """
        return [f.name for f in self]

    def show(self):
        """ Show a nicely formatted list of available formats
        """
        print(self)
