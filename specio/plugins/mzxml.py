"""Plugin to read mzXML file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

from os.path import basename

from .. import formats
from ..core import Format
from ..core.util import Spectrum


class MZXML(Format):
    """Plugin to read MZXML file which stores mass spectrometry data.

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

        def _read_mzxml(self, mzxml_filename):
            from pyopenms import MzXMLFile, MSExperiment
            file_handler = MzXMLFile()
            experiment = MSExperiment()
            file_handler.load(mzxml_filename, experiment)
            spectra = []
            for sp in experiment:
                sp_converted = self._build_spectrum(sp)
                if sp_converted is not None:
                    sp_converted.meta.update(
                        {'filename': basename(mzxml_filename)})
                    spectra.append(sp_converted)
            return spectra

        def _open(self):
            self._fp = self.request.get_local_filename()
            self._data = self._read_mzxml(self._fp)

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass


format = MZXML('MZXML',
               'mzXML Mass Spectrometry data format',
               '.mzxml')
formats.add_format(format)
