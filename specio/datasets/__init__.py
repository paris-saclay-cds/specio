"""
The module `specio.datasets` includes some toy file which are supported by
the plugins reader.
"""

from .path import load_csv_path
from .path import load_fsm_path
from .path import load_mzml_path
from .path import load_sp_path
from .path import load_spc_path


__all__ = ['load_csv_path',
           'load_fsm_path',
           'load_mzml_path',
           'load_sp_path',
           'load_spc_path']
