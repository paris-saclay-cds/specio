"""Python input/output for spectroscopic files."""

from .core import FormatManager

formats = FormatManager()

from ._version import __version__

__all__ = ['__version__']

del FormatManager
