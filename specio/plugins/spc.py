"""Plugin to read SPC file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

import struct
import warnings

import numpy as np

import spc

from .. import formats
from ..core import Format
from ..core.exceptions import VersionError
from ..core.request import read_n_bytes
from ..core.util import Spectrum

VERSION_SUPPORTED = (b'\x4b', b'\x4d', b'\xcf')


class SPC(Format):
    """Plugin to read SPC file.

    Parameters
    ----------

    Attributes
    ----------

    """

    def _can_read(self, request):
        if request.mode in (self.modes + '?'):
            if request.filename.lower().endswith(self.extensions):
                # check that the first byte contain a version supported by spc
                content = read_n_bytes(request.get_file(), 2)
                _, version = struct.unpack('<cc'.encode('utf8'), content)
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
            if spc_file.fversn == b'\x4b':
                meta = {'ftflg': spc_file.ftflg,
                        'fversn': spc_file.versn
                        'fexpr': spc_file.fexper,
                        'fexp' : spc_file.fexp,
                        'fnpts': spc_file.fnpts,
                        'ffirst': spc_file.ffirst,
                        'flast': spc_file.flast,
                        'fnsuv': spc_file.fnsub,
                        'fxtype': spc_file.fxtype,
                        'fytype': spc_file.fytype,
                        'fztype': spc_file.fztype,
                        'fpost': spc_file.fpost,
                        'fdate': spc_file.fdate,
                        'fres': spc_file.fres,
                        'fsource': spc_file.fsource,
                        'fpeakpt': spc_file.fpeakpt,
                        'fspare': spc_file.fspare,
                        'fcmnt': spc_file.fcmnt,
                        'fcatxt': spc_file.fcatxt,
                        'flogoff': spc_file.flogoff,
                        'fmods': spc_file.fmods,
                        'fprocs': spc_file.fprocs,
                        'flevel': spc_file.flevel,
                        'fsamplin': spc_file.fsampin,
                        'ffactor': spc_file.ffactor,
                        'fmethod': spc_file.fmethod,
                        'fzinc': spc_file.fzinc,
                        'fwplanes': spc_file.fwplanes,
                        'fwinc': spc_file.fwinc,
                        'fwtype': spc_file.fwtype,
                        'freserv': spc_file.freserv,
                        'tsprec': spc_file.tsprec,
                        'tcgram': spc_file.tcgram,
                        'tmulti': spc_file.tmulti,
                        'trandm': spc_file.trandm,
                        'tordrd': spc_file.tordrd,
                        'talabs': spc_file.talabs,
                        'txyxys': spc_file.txyxys,
                        'txvals': spc_file.txvals,
                        'year' : spc_file.year,
                        'month': spc_file.month,
                        'day': spc_file.day,
                        'hour': spc_file.hour,
                        'minute': spc_file.minute,
                        'cmnt': spc_file.cmnt,
                        'dat_multi': spc_file.dat_multi,
                        'dat_fmt': spc_file.dat_fmt,
                        'logsizd': spc_file.logsizd,
                        'logsizm': spc_file.logsizm,
                        'logtxto': spc_file.logtxto,
                        'logbins': spc_file.logbins,
                        'logdsks': spc_file.logdsks,
                        'logspar': spc_file.logspar,
                        'log_dict': spc_file.log_dict,
                        'spacing': spc_file.spacing}
            elif spc_file.fversn == b'\x4d':
                meta = {'oftflgs': spc_file.oftflgs,
                        'oversn': spc_file.oversn,
                        'oexp': spc_file.oexp,
                        'onpts': spc_file.onpts,
                        'ofirst': spc_file.ofirst,
                        'olast': spc_file.olast,
                        'fxtype': spc_file.fxtype,
                        'fytype': spc_file.fytype,
                        'oyear': spc_file.oyear,
                        'omonth': spc_file.omonth,
                        'oday': spc_file.oday,
                        'ohour': spc_file.ohour,
                        'ominute': spc_file.ominute,
                        'ores': spc_file.ores,
                        'opeakpt': spc_file.opeakpt,
                        'onscans': spc_file.onscans,
                        'ospare': spc_file.ospare,
                        'ocmnt': spc_file.ocmnt,
                        'ocatxt': spc_file.ocatxt,
                        'osubh1': spc_file.osubh1,
                        'tsprec': spc_file.tsprec,
                        'tcgram': spc_file.tcgram,
                        'tmulti': spc_file.tmulti,
                        'trandm': spc_file.trandm,
                        'tordrd': spc_file.tordrd,
                        'talabs': spc_file.talabs,
                        'txyxys': spc_file.txyxys,
                        'txvals': spc_file.txvals,
                        'fztype': spc_file.fztype}
            else:
                meta = {}

            return meta

        @staticmethod
        def _spc_to_numpy(spc_file):
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
            if (spc_file.dat_fmt == 'gx-y' or
                    spc_file.dat_fmt == 'x-y'):
                wavelength = spc_file.x
            elif spc_file.dat_fmt == '-xy':
                wavelength = np.array([f.x for f in spc_file.sub])
            spectrum = np.array([f.y for f in spc_file.sub])
            meta = self._meta_data_from_spc(spc_file)

            return Spectrum(spectrum, wavelength, meta)

        def _open(self):
            # Open the reader
            self._fp = self.request.get_filename()
            self._data = self._spc_to_numpy(spc.File(self._fp))

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            self._fp = None
            self._data = None

        def _get_length(self):
            # Give the number of spectra
            return self._length

        def _get_data(self, index):
            if len(self._data.spectrum.shape) == 2:
                if len(self._data.wavelength.shape) == 1:
                    return (self._data.spectrum[index, :],
                            self._data.wavelength,
                            self._data.meta)
                else:
                    return (self._data.spectrum[index, :],
                            self._data.wavelength[index, :],
                            self._data.meta)
            else:
                return (self._data.spectrum[index],
                        self._data.wavelength[index],
                        self._data.meta)

        def _get_meta_data(self, index):
            return self._data.meta


# Register. You register an *instance* of a Format class. Here specify:
format = SPC('SPC',
             'Galactic Industries Corporation SPC binary format',
             '.spc',
             'sS')
formats.add_format(format)
