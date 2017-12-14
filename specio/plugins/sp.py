"""Plugin to read SP file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

import struct

import numpy as np

from .. import formats
from ..core import Format
from ..core import Spectrum


def _block_info(data):
    """Retrieve the information of the next block.

    The block ID is represented by an unsigned short while the block size is
    represented by a signed int.

    Parameters
    ----------
    data : bytes, length=6
        Data containing the block information

    Returns
    -------
    block_id : int
        The block ID.

    block_size :
        The size of the block.

    """
    # check that the data is an array of bytes
    if len(data) != 6:
        raise ValueError("'data' should be 6 bytes. Got {} instead.".format(
            len(data)))
    return struct.unpack('<Hi', data)


class SP(Format):
    """Plugin to read SP file which stores IR spectroscopic data.

    The file format is used by Perkin Elmer IR instrument.

    Parameters
    ----------
    Specify arguments in numpy doc style here.

    Attributes
    ----------
    Specify the specific attributes that can be useful.

    """

    def _can_read(self, request):
        if request.filename.lower().endswith(self.extensions):
            # the 4 first bytes of a fsm file corresponds to PEPE
            if request.firstbytes[:4] == b'PEPE':
                return True
        return False
    # -- reader

    class Reader(Format.Reader):

        @staticmethod
        def _read_sp(sp_file):
            """Read the sp file.

            Parameters
            ----------
            sp_file : file object
                The file object in byte mode.

            Returns
            -------
            spectrum : Spectrum
                Returns a Spectrum instance.

            """
            content = sp_file.read()

            start_byte = 0
            n_bytes = 4
            signature = content[start_byte:start_byte + n_bytes]

            start_byte += n_bytes
            # the description is fixed to 40 bytes
            n_bytes = 40
            description = content[
                start_byte:start_byte + n_bytes].decode('utf8')

            meta = {'signature': signature,
                    'description': description}
            spectrum = []

            NBP = []
            start_byte += n_bytes
            n_bytes = 6
            block_id, block_size = _block_info(
                content[start_byte:start_byte + n_bytes])
            NBP.append(start_byte + n_bytes + block_size)
            start_byte += n_bytes
            while block_id != 122:
                n_bytes = 4
                block_id = struct.unpack('<HH', content[start_byte:
                                                        start_byte + n_bytes])
                if block_id[1] == 'u':
                    print('HERE')
                    start_byte = NBP[-1]
                    NBP = NBP[:-1]
                    while start_byte >= NBP[-1]:
                        NBP = NBP[-1]
                else:
                    n_bytes = 6
                    block_id, block_size = _block_info(
                        content[start_byte:start_byte + n_bytes])
                    NBP.append(start_byte + n_bytes + block_size)
                    start_byte += n_bytes


            return Spectrum(spectrum, wavelength, meta)

        def _open(self):
            self._fp = self.request.get_file()
            self._data = self._read_sp(self._fp)
            self._length = self._data.spectrum.shape[0]

        def _close(self):
            pass

        def _get_length(self):
            return self._length

        def _get_meta_data(self, index):
            self._data.meta


format = SP('SP',
            'SP Perkin Elmer binary format.',
            '.sp')
formats.add_format(format)
