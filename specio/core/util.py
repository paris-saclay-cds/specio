"""Utilities"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import re
from collections import OrderedDict

from six import string_types


class Dict(OrderedDict):
    """ A dict in which the keys can be get and set as if they were
    attributes. Very convenient in combination with autocompletion.

    This Dict still behaves as much as possible as a normal dict, and
    keys can be anything that are otherwise valid keys. However,
    keys that are not valid identifiers or that are names of the dict
    class (such as 'items' and 'copy') cannot be get/set as attributes.
    """

    __reserved_names__ = dir(OrderedDict())  # Also from OrderedDict
    __pure_names__ = dir(dict())

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            if key in self:
                return self[key]
            else:
                raise

    def __setattr__(self, key, val):
        if key in Dict.__reserved_names__:
            # Either let OrderedDict do its work, or disallow
            if key not in Dict.__pure_names__:
                return OrderedDict.__setattr__(self, key, val)
            else:
                raise AttributeError('Reserved name, this key can only ' +
                                     'be set via ``d[%r] = X``' % key)
        else:
            # if isinstance(val, dict): val = Dict(val) -> no, makes a copy!
            self[key] = val

    @staticmethod
    def _isidentifier(val):
        return bool(re.match(r'[a-z_]\w*$', val, re.I))

    def __dir__(self):
        names = [k for k in self.keys() if
                 (isinstance(k, string_types) and self._isidentifier(k))]
        return Dict.__reserved_names__ + names


class Spectrum(object):
    """Class containing the spectrum information.

    This data structure is used and returned by :func:`specio.specread`.

    Parameters
    ----------
    amplitudes : ndarray, shape (n_wavelength) or (n_spectra, n_wavelength)
        The amplitudes or counts.

    wavelength : ndarray, shape (n_wavelength,)
        The corresponding wavelength.

    meta : dict
        The dictionary containing the meta data.

    Notes
    -----
    See :ref:`sphx_glr_auto_examples_plot_spectrum_usage.py`.

    """

    @staticmethod
    def _validate_amplitudes_wavelength(amplitudes, wavelength):
        msg = ("The number of frequencies in wavelength and spectra are"
               " not equal. Wavelength: {} - Amplitudes: {}.")
        if wavelength.ndim == 1 and amplitudes.ndim == 2:
            if wavelength.shape[0] != amplitudes.shape[1]:
                raise ValueError(msg.format(wavelength.shape[0],
                                            amplitudes.shape[1]))
        elif wavelength.ndim == 1 and amplitudes.ndim == 1:
            if wavelength.size != amplitudes.size:
                raise ValueError(msg.format(wavelength.size,
                                            amplitudes.size))
        else:
            raise ValueError("The dimension of wavelength and amplitudes are"
                             " incorrect. They need to be 1-D or 2-D."
                             " Wavelength {} - Amplitudes: {}".format(
                                 wavelength.shape, amplitudes.shape))

        return amplitudes, wavelength

    def __init__(self, amplitudes, wavelength, meta=None):
        self.amplitudes, self.wavelength = \
            self._validate_amplitudes_wavelength(amplitudes, wavelength)
        self.meta = meta if meta is not None else {}

    def __len__(self):
        if self.amplitudes.ndim == 1:
            return 1
        else:
            return self.amplitudes.shape[0]

    def __repr__(self):
        msg = ("Spectrum: \n"
               "wavelength:\n {} \n"
               "amplitudes: \n {} \n"
               "metadata: \n {} \n".format(self.wavelength,
                                           self.amplitudes,
                                           self.meta))
        return msg
