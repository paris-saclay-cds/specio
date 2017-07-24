"""Utilities"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import re
from collections import OrderedDict
from six import string_types

import numpy as np


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

    Parameters
    ----------
    spectrum : ndarray, shape (n_spectra, n_wavelength)
        The spectrum read.

    wavelength : ndarray, shape (n_wavelength,) or (n_spectra, n_wavelength)
        The corresponding wavelength.

    meta : dict
        The dictionary containing the meta data.
    """

    @staticmethod
    def _validate_spectrum_wavelength(spectrum, wavelength):
        # x-y format / gx-y format
        # wavelentgh : shape (n_wavelength,)
        # spectrum : shape (n_spectra, n_wavelength)
        if len(wavelength.shape) == 1 and len(spectrum.shape) == 2:
            if wavelength.shape[0] != spectrum.shape[1]:
                raise ValueError("The number of frequencies in wavelength and"
                                 " spectra are not equal. Wavelength: {} -"
                                 " Spectrum: {}".format(wavelength.shape[0],
                                                        spectrum.shape[1]))
        # -xy format
        # wavelength : shape (n_spectra, n_wavelength)
        # spectrum : shape (n_spectra, n_wavelength)
        elif len(wavelength.shape) == 2 and len(spectrum.shape) == 2:
            if wavelength.shape != spectrum.shape:
                raise ValueError("The dimension of wavelength and spectrum are"
                                 " not equal. Wavelength: {} - Spectrum:"
                                 " {}".format(wavelength.shape,
                                              spectrum.shape))
        # -xy format
        # wavelength : shape (n_spectra,) of shape (n_wavelength,)
        # spectrum : shape (n_spectra,) of shape (n_wavelength,)
        elif len(wavelength.shape) == 1 and len(spectrum.shape) == 1:
            if wavelength.shape != spectrum.shape:
                raise ValueError("The number of spectra in wavelength and"
                                 " spectra are not equal. Wavelength: {} -"
                                 " Spectrum: {}".format(wavelength.shape,
                                                        spectrum.shape))
            for wave, spectra in zip(wavelength, spectrum):
                if wave.shape != spectra.shape:
                    raise ValueError("The number of wavelength in wavelength "
                                     " and spectra are not equal. Wavelength: "
                                     " {} - Spectrum: {}".format(
                                         wave.shape, spectra.shape))
        else:
            raise ValueError("The dimension of wavelength and spectrum are"
                             " incorrect. They need to be 1-D or 2-D."
                             " Wavelength {} - Spectrum: {}".format(
                                 wavelength.shape, spectrum.shape))

        return spectrum, wavelength

    def __init__(self, spectrum, wavelength, meta=None):
        if not isinstance(spectrum, np.ndarray):
            raise ValueError('Spectrum expects spectrum to be a numpy array.')
        if not isinstance(wavelength, np.ndarray):
            raise ValueError('Spectrum expects wavelength to be a numpy'
                             ' array.')
        if not (meta is None or isinstance(meta, dict)):
            raise ValueError('Spectrum expects meta data to be a dict.')

        self.spectrum, self.wavelength = self._validate_spectrum_wavelength(
            spectrum, wavelength)
        self.meta = meta if meta is not None else {}

    def __repr__(self):
        msg = ("Spectrum: \n"
               "wavelength:\n {} \n"
               "spectra: \n {} \n"
               "metadata: \n {} \n".format(self.wavelength,
                                           self.spectrum,
                                           self.meta))
        return msg
