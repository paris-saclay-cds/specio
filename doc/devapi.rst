----------------------
Specio's developer API
----------------------

..
    We just import the whole of specio.core
    The imageio.core docstring and __all__ are modified in
    at the init of documenation building to make this show
    all members and give a nice overview.

This page lists the developer documentation for specio. Normal users
will generally not need this, except perhaps the :class:`.Format` class.
All these functions and classes are available in the ``specio.core``
namespace.


.. currentmodule:: specio.core

.. autosummary::
   :toctree: generated/

   Format
   FormatManager
   Request
   Dict
   Spectrum
   CannotReadSpectraError
