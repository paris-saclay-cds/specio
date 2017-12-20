"""Plugin to read SP file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

import struct
from os.path import basename

import numpy as np
from six import string_types, indexbytes

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


def _decode_5104(data):
    """Read the block of data with ID 5104.

    Parameters
    ----------
    data : bytes
        The 5104 block to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """

    text = []
    start_byte = 0
    while start_byte + 2 < len(data):
        tag = data[start_byte:start_byte + 2]
        if tag == b'#u':
            start_byte += 2
            text_size = struct.unpack(
                '<h', data[start_byte:start_byte + 2])[0]
            start_byte += 2
            text.append(data[start_byte:start_byte + text_size].decode('utf8'))
            start_byte += text_size
            start_byte += 6
        elif tag == b'$u':
            start_byte += 2
            text.append(struct.unpack(
                '<h', data[start_byte:start_byte + 2])[0])
            start_byte += 2
            start_byte += 6
        elif tag == b',u':
            start_byte += 2
            text.append(struct.unpack(
                '<h', data[start_byte:start_byte + 2])[0])
            start_byte += 2
        else:
            start_byte += 1

    return {'analyst': text[0],
            'date': text[2],
            'image_name': text[4],
            'instrument_model': text[5],
            'instrument_serial_number': text[6],
            'instrument_software_version': text[7],
            'accumulations': text[9],
            'detector': text[11],
            'source': text[12],
            'beam_splitter': text[13],
            'apodization': text[15],
            'spectrum_type': text[16],
            'beam_type': text[17],
            'phase_correction': text[20],
            'ir_accessory': text[26],
            'igram_type': text[28],
            'scan_direction': text[29],
            'background_scans': text[32]}


def _decode_25739(data):
    """Read the block of data with ID 25739.

    Parameters
    ----------
    data : bytes
        The 25739 block to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """
    start_byte = 0
    n_bytes = 2
    var_id = struct.unpack('<H', data[start_byte:start_byte + n_bytes])[0]
    if var_id == 29987:
        start_byte += n_bytes
        n_bytes = 2
        var_size = struct.unpack('<H', data[start_byte:
                                            start_byte + n_bytes])[0]
        start_byte += n_bytes
        n_bytes = var_size
        return {'file_path': data[start_byte:
                                  start_byte + n_bytes].decode('utf-8')}


def _decode_35698(data):
    """Read the block of data with ID 35698.

    Parameters
    ----------
    data : bytes
        The 35698 block to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """
    start_byte = 0
    n_bytes = 2
    var_id = struct.unpack('<H', data[start_byte:start_byte + n_bytes])[0]
    if var_id == 29981:
        start_byte += n_bytes
        n_bytes = 16
        min_wavelength, max_wavelength = struct.unpack(
            '<dd', data[start_byte:start_byte + n_bytes])
    return {'min_wavelength': min_wavelength,
            'max_wavelength': max_wavelength}


def _decode_35699(data):
    """Read the block of data with ID 35699.

    Parameters
    ----------
    data : bytes
        The 35699 block to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """
    start_byte = 0
    n_bytes = 2
    var_id = struct.unpack('<H', data[start_byte:start_byte + n_bytes])[0]
    if var_id == 29981:
        start_byte += n_bytes
        n_bytes = 16
        min_absolute, max_absolute = struct.unpack(
            '<dd', data[start_byte:start_byte + n_bytes])
    return {'min_absolute': min_absolute,
            'max_absolute': max_absolute}


def _decode_35700(data):
    """Read the block of data with ID 35700.

    Parameters
    ----------
    data : bytes
        The 35700 block to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """
    start_byte = 0
    n_bytes = 2
    var_id = struct.unpack('<H', data[start_byte:start_byte + n_bytes])[0]
    if var_id == 29979:
        start_byte += n_bytes
        n_bytes = 8
        wavelength_step = struct.unpack(
            '<d', data[start_byte:start_byte + n_bytes])[0]
    return {'wavelength_step': wavelength_step}


def _decode_35701(data):
    """Read the block of data with ID 35701.

    Parameters
    ----------
    data : bytes
        The 35701 block to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """
    start_byte = 0
    n_bytes = 2
    var_id = struct.unpack('<H', data[start_byte:start_byte + n_bytes])[0]
    if var_id == 29995:
        start_byte += n_bytes
        n_bytes = 4
        n_points = struct.unpack(
            '<I', data[start_byte:start_byte + n_bytes])[0]
    return {'n_points': n_points}


def _decode_35708(data):
    """Read the block of data with ID 35708.

    Parameters
    ----------
    data : bytes
        The 35708 block to decode.

    Returns
    -------
    data : ndarray
        The extracted data.

    """
    start_byte = 0
    n_bytes = 2
    var_id = struct.unpack('<H', data[start_byte:start_byte + n_bytes])[0]
    if var_id == 29974:
        start_byte += n_bytes
        n_bytes = 4
        var_size = struct.unpack('<I', data[start_byte:
                                            start_byte + n_bytes])[0]
        start_byte += n_bytes
        n_bytes = var_size

        return np.frombuffer(data[start_byte:start_byte + n_bytes],
                             dtype=np.float64)


FUNC_DECODE = {25739: _decode_25739,
               35698: _decode_35698,
               35699: _decode_35699,
               35700: _decode_35700,
               35701: _decode_35701,
               35708: _decode_35708}


class SP(Format):
    """Plugin to read SP file which stores IR spectroscopic data.

    The file format is used by Perkin Elmer IR instrument.

    Notes
    -----
    See :ref:`sphx_glr_auto_examples_reader_plot_read_sp.py`.

    Examples
    --------
    >>> from specio import specread
    >>> from specio.datasets import load_sp_path
    >>> spectra = specread(load_sp_path())
    >>> spectra.wavelength
    array([ 4000.,  3999.,  3998., ...,   702.,   701.,   700.])
    >>> spectra.amplitudes # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    array([ 0.03723936,  0.03718614,  0.03713289, ...,  0.00313506,
            0.00368404,  0.00417556])

    """

    def _can_read(self, request):
        if request.filename.lower().endswith(self.extensions):
            # the 4 first bytes of a sp file corresponds to PEPE
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
            start_byte += n_bytes
            NBP.append(start_byte + block_size)
            while block_id != 122 and start_byte < len(content) - 2:
                next_block_id = content[start_byte:start_byte + 2]
                if indexbytes(next_block_id, 1) == 117:
                    start_byte = NBP[-1]
                    NBP = NBP[:-1]
                    while start_byte >= NBP[-1]:
                        NBP = NBP[-1]
                else:
                    block_id, block_size = _block_info(
                        content[start_byte:start_byte + n_bytes])
                    start_byte += n_bytes
                    NBP.append(start_byte + block_size)

            meta.update(_decode_5104(
                content[start_byte:start_byte + block_size]))

            start_byte = NBP[1]
            while start_byte < len(content):
                n_bytes = 6
                block_id, block_size = _block_info(
                    content[start_byte:start_byte + n_bytes])
                start_byte += n_bytes
                if block_id in FUNC_DECODE.keys():
                    decoded_data = FUNC_DECODE[block_id](
                        content[start_byte:start_byte + block_size])
                    if isinstance(decoded_data, dict):
                        meta.update(decoded_data)
                    else:
                        spectrum = decoded_data
                start_byte += block_size

            wavelength = np.linspace(meta['min_wavelength'],
                                     meta['max_wavelength'],
                                     meta['n_points'])

            if isinstance(sp_file, string_types):
                meta['filename'] = basename(sp_file)
            else:
                meta['filename'] = basename(sp_file.name)

            return Spectrum(spectrum, wavelength, meta)

        def _open(self):
            self._fp = self.request.get_file()
            self._data = self._read_sp(self._fp)

        def _close(self):
            pass


format = SP('SP',
            'SP Perkin Elmer binary format.',
            '.sp')
formats.add_format(format)
