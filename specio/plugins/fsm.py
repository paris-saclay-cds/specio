"""Plugin to read FSM file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

import numpy as np

from .. import formats
from ..core import Format
from ..core.util import Spectrum
from ._fsm import _block_info, _decode_5100, _decode_5104, _decode_5105


FUNC_DECODE = {5100: _decode_5100,
               5104: _decode_5104,
               5105: _decode_5105}


class FSM(Format):
    """Plugin to read FSM file which store IR spectroscopic data.

    This file format is used by Perkin Elmer Spotlight IR instrument.

    Examples
    --------

    """

    def _can_read(self, request):
        if request.filename.lower().endswith(self.extensions):
            if request.firstbytes[:4] == b'PEPE':
                return True
        return False
    # -- reader

    class Reader(Format.Reader):

        @staticmethod
        def _read_fsm(fsm_file):
            """Read the fsm file.

            Parameters
            ----------
            fsm_file : file object
                The file object in bytes mode.

            Returns
            -------
            spectrum : Spectrum
                Return a Spectrum instance.

            """
            content = fsm_file.read()

            start_byte = 0
            n_bytes = 4
            signature = content[start_byte:start_byte + n_bytes]

            start_byte += n_bytes
            n_bytes = 40
            description = content[
                start_byte:start_byte + n_bytes].decode('utf8')

            meta = {'signature': signature,
                    'description': description}
            spectrum = []

            while start_byte + n_bytes < len(content):
                # read block info
                start_byte += n_bytes
                n_bytes = 6
                block_id, block_size = _block_info(
                    content[start_byte:start_byte + n_bytes])
                # read the meta data
                start_byte += n_bytes
                n_bytes = block_size
                data_extracted = FUNC_DECODE[block_id](
                    content[start_byte:start_byte + n_bytes])
                if isinstance(data_extracted, dict):
                    meta.update(data_extracted)
                else:
                    spectrum.append(data_extracted)

            spectrum = np.array(spectrum)
            # we add a value such that we include the endpoint
            wavelength = np.arange(meta['z_start'],
                                   meta['z_end'] + meta['z_delta'],
                                   meta['z_delta'])

            return Spectrum(spectrum, wavelength, meta)

        def _open(self, some_option=False, length=1):
            self._fp = self.request.get_file()
            self._data = self._read_fsm(self._fp)
            self._length = self._data.spectrum.shape[0]

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            self._data = None
            self._length = None

        def _get_length(self):
            # Return the number of spectra
            return self._length

        def _get_meta_data(self, index):
            return self._data.meta


format = FSM('FSM',
             'FSM Perkin Elmer Spotlight IR instrument binary format',
             '.fsm')
formats.add_format(format)
