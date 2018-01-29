"""Plugin to read mzml file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

from os.path import basename

from .. import formats
from ..core import Format
from ..core.util import Spectrum


class MZML(Format):
    """Plugin to read MZML file which stores mass spectrometry data.

    This file format is used to store mass spectrometry data.

    Notes
    -----

    Examples
    --------

    """

    def _can_read(self, request):
        if request.filename.lower().endswith(self.extensions):
            return True
        return False
    # -- reader

    class Reader(Format.Reader):

        @staticmethod
        def _build_spectrum(spectra):
            keys = []
            spectra.getKeys(keys)
            meta = {str(key.decode('utf-8')): spectra.getMetaValue(key)
                    for key in keys}
            wavelength, amplitudes = spectra.get_peaks()
            if wavelength.size:
                return Spectrum(amplitudes, wavelength, meta)
            else:
                return None

        def _read_mzml(self, mzml_filename):
            from pyopenms import MzMLFile, MSExperiment
            file_handler = MzMLFile()
            experiment = MSExperiment()
            file_handler.load(mzml_filename, experiment)
            spectra = []
            for sp in experiment:
                sp_converted = self._build_spectrum(sp)
                if sp_converted is not None:
                    sp_converted.meta.update(
                        {'filename': basename(mzml_filename)})
                    spectra.append(sp_converted)
            return spectra

        def _open(self):
            self._fp = self.request.get_local_filename()
            self._data = self._read_mzml(self._fp)

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass


format = MZML('MZML',
              'MZML Mass Spectrometry data format',
              '.mzml')
formats.add_format(format)
