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

    wavelength : ndarray, shape (n_wavelength,)
        The corresponding wavelength.

    meta : dict
        The dictionary containing the meta data.
    """

    def __init__(self, spectrum, wavelength, meta=None):
        if not isinstance(spectrum, np.ndarray):
            raise ValueError('Spectrum expects spectrum to be a numpy array.')
        if not isinstance(wavelength, np.ndarray):
            raise ValueError('Spectrum expects wavelength to be a numpy'
                             ' array.')
        if not (meta is None or isinstance(meta, dict)):
            raise ValueError('Spectrum expects meta data to be a dict.')
        meta = meta if meta is not None else {}

    def _copy_meta(self, meta):
        """ Make a 2-level deep copy of the meta dictionary.
        """
        self._meta = Dict()
        for key, val in meta.items():
            if isinstance(val, dict):
                val = Dict(val)  # Copy this level
        self._meta[key] = val

    def __array_finalize__(self, ob):
        """ So the meta info is maintained when doing calculations with
        the array.
        """
        if isinstance(ob, Spectrum):
            self._copy_meta(ob.meta)
        else:
            self._copy_meta({})

    def __array_wrap__(self, out, context=None):
        """ So that we return a native numpy array (or scalar) when a
        reducting ufunc is applied (such as sum(), std(), etc.)
        """
        if not out.shape:
            return out.dtype.type(out)  # Scalar
        elif out.shape != self.shape:
            return out.view(type=np.ndarray)
        else:
            return out # Type Spectrum
