"""Plugin to read CSV file."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

from __future__ import absolute_import, print_function, division

from .. import formats
from ..core import Format
from ..core.util import Spectrum


class CSV(Format):
    """Plugin to read CSV file which is the format exported using
    :func:`specio.core.Spectrum.to_csv`.

    The CSV format is the Comma-Separated Values format [1]_.

    Notes
    -----
    See :ref:`sphx_glr_auto_examples_reader_plot_read_csv.py`.

    Examples
    --------
    >>> from specio import specread
    >>> from specio.datasets import load_csv_path
    >>> spectra = specread(load_csv_path())
    >>> spectra.wavelength
    array([  400.19921875,   402.72982788,   405.25958252, ...,  3795.59448242,
            3797.11914062,  3798.64355469])
    >>> spectra.amplitudes # doctest: +NORMALIZE_WHITESPACE
    array([[ 173.33334351,  187.33332825,  188.33332825, ...,  107.15319061,
             106.04219055,  109.70896912],
           [ 191.1111145 ,  203.222229  ,  201.777771  , ...,  108.46702576,
             101.90904236,  105.12884521],
           [ 195.777771  ,  214.66668701,  206.33332825, ...,  100.96577454,
             101.17821503,  101.50177002],
           ...,
           [ 206.11109924,  215.777771  ,  219.99998474, ...,  104.60214233,
             106.93334961,  102.82010651],
           [ 201.33332825,  209.777771  ,  210.33331299, ...,   99.27733612,
             101.49320221,  103.26461029],
           [ 201.1111145 ,  206.1111145 ,  209.44444275, ...,  104.57073212,
             102.45584106,   99.34095001]])

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Comma-separated_values

    """

    def _can_read(self, request):
        if request.filename.lower().endswith(self.extensions):
            return True
        return False
    # -- reader

    class Reader(Format.Reader):

        def _read_csv(self, csv_file):
            import pandas as pd
            df_data = pd.read_csv(self._fp, index_col=0)
            df_data.columns = df_data.columns.astype(float)
            spectrum = df_data.values.squeeze()
            wavelength = df_data.columns.values
            index = df_data.index.values
            if index.size > 1:
                meta = tuple({'filename': idx} for idx in index)
            else:
                meta = {'filename': index[0]}
            return Spectrum(spectrum, wavelength, meta)

        def _open(self):
            # Open the reader
            self._fp = self.request.get_file()
            self._data = self._read_csv(self._fp)

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass


# Register. You register an *instance* of a Format class. Here specify:
format = CSV('CSV',
             'Internal Comma-Separated Values format',
             '.csv')
formats.add_format(format)
