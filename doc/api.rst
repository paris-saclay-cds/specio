###################
specio's user API
###################

Spectra reader functions
========================

These functions represent specio's main interface for the user. They provide a
common API to read spectra data for a large variety of formats. All read
functions accept keyword arguments, which are passed on to the format that does
the actual work.  To see what keyword arguments are supported by a specific
format, use the :func:`.help` function.

Functions for reading:

  * :func:`.specread` - read a file with spectra from the specified uri

For a larger degree of control, specio provides a function
:func:`.get_reader`. It returns an :class:`.Reader` object, which can be used
to read data and meta data in a more controlled manner.  This also allows
specific scientific formats to be exposed in a way that best suits that
file-format.

Functions
---------

.. autosummary::
   :toctree: generated/
   :template: function.rst

   specio.help
   specio.show_formats
   specio.specread
   specio.get_reader

Classes
-------

.. autosummary::
   :toctree: generated/
   :template: class.rst

   specio.core.format.Reader

Core data structure
===================

:func:`specio.specread` will return either a list of instances or an instance
from the class :class:`specio.core.Spectrum`. This class is composed of three
attributes:

* a 1D ndarray of shape (n_wavelength,) or 2D ndarray of shape
  (n_spectra, n_wavelength) ``amplitudes`` containing the counts/amplitude for
  the different wavelengths;
* a 1D ndarray of shape (n_wavelength,) ``wavelength`` containing the
  wavelength for which the spectra have been acquired;
* a dictionary ``meta`` containing the metadata.

For more information, you can check the full API documentation above.

.. autosummary::
   :toctree: generated/
   :template: class.rst

   specio.core.Spectrum

Example datasets
================

.. automodule:: specio.datasets
    :no-members:
    :no-inherited-members:

.. currentmodule:: specio

.. autosummary::
   :toctree: generated/
   :template: function.rst

   datasets.load_spc_path
   datasets.load_fsm_path
