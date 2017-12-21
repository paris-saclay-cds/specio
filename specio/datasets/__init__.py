"""
The module `specio.datasets` includes some toy file which are supported by
the plugins reader.
"""

from .fsm import load_fsm_path
from .mzml import load_mzml_path
from .sp import load_sp_path
from .spc import load_spc_path


__all__ = ['load_fsm_path',
           'load_mzml_path',
           'load_sp_path',
           'load_spc_path']
