"""Private function used to read FSM file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import binascii
import struct


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
    return struct.unpack('<Hi'.encode('utf8'), data)


def _decode_5100(data):
    """Read the block of data with ID 5100.

    Parameters
    ----------
    data : bytes
        The 5100 black to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """
    name_size = struct.unpack('<h'.encode('utf8'),
                              data[:2])[0]
    name_format = '<' + 'B' * name_size
    name = struct.unpack(name_format.encode('utf8'), data[2:name_size + 2])
    header_format = '<ddddddddddiiihBhBhBhB'
    header_size = 104

    (x_delta, y_delta, z_delta, z_start, z_end, z_4d_start, z_4d_end,
     x_init, y_init, z_init, n_x, n_y, n_z, _, text1, _, text2, resolution,
     text3, transmission, text4) = struct.unpack(
         header_format.encode('utf8'),
         data[name_size + 2:name_size + header_size + 2])

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
    """Read the block of data with ID 5100.

    Parameters
    ----------
    data : bytes
        The 5100 black to decode.

    Returns
    -------
    meta : dict
        The extracted information.

    """

    text = []
    start_byte = 0
    while start_byte + 2 < len(data):
        tag = binascii.hexlify(data[start_byte:start_byte + 2])
        if tag == b'2375':
            start_byte += 2
            text_size = struct.unpack('<h'.encode('utf8'),
                                      data[start_byte:start_byte + 2])[0]
            start_byte += 2
            text.append(data[start_byte:start_byte + text_size].decode('utf8'))
            start_byte += text_size
            start_byte += 6
        elif tag == b'2475':
            start_byte += 2
            text.append(struct.unpack(
                '<h'.encode('utf8'),
                data[start_byte:start_byte + 2])[0])
            start_byte += 2
            start_byte += 6
        elif tag == b'2c75':
            start_byte += 2
            text.append(struct.unpack(
                '<h'.encode('utf8'),
                data[start_byte:start_byte + 2])[0])
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

    Parameters
    ----------
    data : bytes
        The 5105 block to be decoded

    Returns
    -------
    spectra : list
        The list of the value decoded.

    """
    data_format = '<' + 'f' * (len(data) // 4)
    return list(struct.unpack(data_format.encode('utf8'), data))
