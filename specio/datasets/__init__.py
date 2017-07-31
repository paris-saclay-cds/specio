"""
The module `specio.datasets` includes some toy file which are supported by
the plugins reader.
"""

from .fsm import load_fsm_path
from .spc import load_spc_path


__all__ = ['load_fsm_path',
           'load_spc_path']
