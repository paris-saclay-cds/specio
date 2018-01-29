"""Plugin to read FSM file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

import struct
from os.path import basename

import numpy as np
from six import string_types

from .. import formats
from ..core import Format
from ..core.util import Spectrum


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


def _decode_5100(data):
    """Read the block of data with ID 5100.

    Parameters
    ----------
    data : bytes
        The 5100 block to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """
    name_size = struct.unpack('<h',
                              data[:2])[0]
    name = data[2:name_size + 2].decode('utf8')

    header_format = '<ddddddddddiiihBhBhBhB'
    header_size = 104

    (x_delta, y_delta, z_delta, z_start, z_end, z_4d_start, z_4d_end,
     x_init, y_init, z_init, n_x, n_y, n_z, _, text1, _, text2, resolution,
     text3, transmission, text4) = struct.unpack(
         header_format, data[name_size + 2:name_size + header_size + 2])

    return {'name': name,
            'x_delta': x_delta,
            'y_delta': y_delta,
            'z_delta': z_delta,
            'z_start': z_start,
            'z_end': z_end,
            'z_4d_start': z_4d_start,
            'z_4d_end': z_4d_end,
            'x_init': x_init,
            'y_init': y_init,
            'z_init': z_init,
            'n_x': n_x,
            'n_y': n_y,
            'n_z': n_z,
            'text1': text1,
            'text2': text2,
            'resolution': resolution,
            'text3': text3,
            'transmission': transmission,
            'text4': text4}


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
            'background_scans': text[32],
            'ir_laser_wave_number_unit': text[67]}


def _decode_5105(data):
    """Read the block of data with ID 5105.

    The data are stored as 32 bits floats.

    Parameters
    ----------
    data : bytes
        The 5105 block to be decoded

    Returns
    -------
    spectra : list
        The list of the value decoded.

    """
    return np.frombuffer(data, dtype=np.float32)


FUNC_DECODE = {5100: _decode_5100,
               5104: _decode_5104,
               5105: _decode_5105}


class FSM(Format):
    """Plugin to read FSM file which stores IR spectroscopic data.

    This file format is used by Perkin Elmer Spotlight IR instrument.

    Notes
    -----
    See :ref:`sphx_glr_auto_examples_reader_plot_read_fsm.py`.

    Examples
    --------
    >>> from specio import specread
    >>> from specio.datasets import load_fsm_path
    >>> spectra = specread(load_fsm_path())
    >>> spectra.wavelength
    array([ 4000.,  3998.,  3996., ...,   724.,   722.,   720.])
    >>> spectra.amplitudes # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE +SKIP
    array([[  38.65655136,   38.6666069 ,   38.64698792, ...,   39.89584732,
              29.76511383,   28.13317108],
           [  44.61751175,   44.51957703,   44.59909439, ...,   27.84810638,
              48.12566376,   44.58335876],
           [  45.4976387 ,   45.44074631,   45.43001556, ...,  104.77108002,
              83.30805206,   55.3244133 ],
           ...,
           [  81.6805954 ,   81.66387177,   81.57576752, ...,  114.77721405,
             125.94933319,  121.3031311 ],
           [  85.60238647,   85.57183075,   85.57678986, ...,  118.79945374,
             154.56201172,  135.4960022 ],
           [  87.86193085,   87.94794464,   88.03714752, ...,   59.7109108 ,
              76.84341431,  122.54582214]], dtype=float32)

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
            # the description is fixed to 40 bytes
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
                # read the upcoming block
                start_byte += n_bytes
                n_bytes = block_size
                data_extracted = FUNC_DECODE[block_id](
                    content[start_byte:start_byte + n_bytes])
                if isinstance(data_extracted, dict):
                    meta.update(data_extracted)
                else:
                    spectrum.append(data_extracted)

            spectrum = np.squeeze(spectrum)
            # we add a value such that we include the endpoint
            wavelength = np.arange(meta['z_start'],
                                   meta['z_end'] + meta['z_delta'],
                                   meta['z_delta'])
            if isinstance(fsm_file, string_types):
                meta['filename'] = basename(fsm_file)
            else:
                meta['filename'] = basename(fsm_file.name)

            return Spectrum(spectrum, wavelength, meta)

        def _open(self):
            self._fp = self.request.get_file()
            self._data = self._read_fsm(self._fp)

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass


format = FSM('FSM',
             'FSM Perkin Elmer Spotlight IR instrument binary format',
             '.fsm')
formats.add_format(format)
