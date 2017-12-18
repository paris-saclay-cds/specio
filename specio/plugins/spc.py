"""Plugin to read SPC file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

import struct
import warnings

import numpy as np

from .. import formats
from ..core import Format
from ..core.exceptions import VersionError
from ..core.request import read_n_bytes
from ..core.util import Spectrum


VERSION_SUPPORTED = (b'\x4b', b'\x4d', b'\xcf')
IGNORED_ATTRIBUTES = ('x', 'sub')


class SPC(Format):
    """Plugin to read SPC file which store spectrostopic data.

    The SPC file format is a file format in which all kinds of spectroscopic
    data, including amongst others infrared spectra, Raman spectra and UV/VIS
    spectra. The format can be regarded as a database with records of variable
    length and each record stores a different kind of data (instrumental
    information, information on one spectrum of a dataset, the spectrum itself
    or extra logs).

    Examples
    --------
    >>> from specio import specread
    >>> from specio.datasets import load_spc_path
    >>> spectra = specread(load_spc_path())
    x-y(1)
    >>> spectra.wavelength
    array([  400.62109375,   402.94384766,   405.26721191, ...,  3797.08911133,
            3798.45288086,  3799.81542969])
    >>> spectra.spectrum
    array([ 1487.        ,  1385.        ,  1441.        , ...,   147.24124146,
             139.16082764,   134.08041382])

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/SPC_file_format

    """

    def _can_read(self, request):
        if request.filename.lower().endswith(self.extensions):
            # check that the first byte contain a version supported by spc
            content = read_n_bytes(request.get_file(), 256)
            _, version = struct.unpack('<cc'.encode('utf8'), content[:2])
            if version not in VERSION_SUPPORTED:
                raise VersionError("The version {} is not yet supported."
                                   " Current supported version are"
                                   " {}.".format(version,
                                                 VERSION_SUPPORTED))
            if version == b'\xcf':
                warnings.warn("Support for this version is highly"
                              " experimental.")
            return True
        return False
    # -- reader

    class Reader(Format.Reader):

        @staticmethod
        def _meta_data_from_spc(spc_file):
            """Create a dictionary with the metadata.

            Parameters
            ----------
            spc_file : spc.File
                The SPC File to be converted.

            Returns
            -------
            meta : dict
                A dictionary with the meta data.

            """
            meta = {key: val
                    for key, val in spc_file.__dict__.items()
                    if key not in IGNORED_ATTRIBUTES or key.startswith('_')}

            return meta

        def _spc_to_numpy(self, spc_file):
            """Convert the SPC File data to spectrum data.

            Parameters
            ----------
            spc_file : spc.File
                The SPC File to be converted.

            Returns
            -------
            spectrum : util.Spectrum
                The converted data.

            """
            meta = self._meta_data_from_spc(spc_file)
            if spc_file.dat_fmt in ('gx-y', 'x-y'):
                spectrum = np.squeeze([f.y for f in spc_file.sub])
                wavelength = spc_file.x
                return Spectrum(spectrum, wavelength, meta)

            elif spc_file.dat_fmt == '-xy':
                return [Spectrum(f.y, f.x, meta) for f in spc_file.sub]

            else:
                raise ValueError('Unknown file structure.')

        def _open(self):
            import spc
            # Open the reader
            self._fp = self.request.get_local_filename()
            self._data = self._spc_to_numpy(spc.File(self._fp))
            self._length = len(self._data)
            # additionally add the filename to the meta data
            self._data.meta['filename'] = self.request.get_local_filename()

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass

        def _get_length(self):
            # Give the number of spectra
            return self._length

        def _get_meta_data(self, index):
            return self._data.meta


# Register. You register an *instance* of a Format class. Here specify:
format = SPC('SPC',
             'Galactic Industries Corporation binary format',
             '.spc')
formats.add_format(format)
