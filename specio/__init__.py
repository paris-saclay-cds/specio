"""Python input/output for spectroscopic files."""

from ._version import __version__
from .core import FormatManager

formats = FormatManager()

# Load the functions
from .core.functions import help
from .core.functions import get_reader
from .core.functions import specread

# Load all the plugins
from . import plugins

# expose the show method of formats
show_formats = formats.show

__all__ = ['formats',
           'help',
           'get_reader',
           'specread',
           'plugins',
           '__version__']

del FormatManager
