"""
====================================================
Read SPC Galactic Industries Corporation binary file
====================================================

This example shows how to read SPC file and plot the results.

"""

# Authors: Guillaume Lemaitre <guillaume.lemaire@inria.fr>
# License: BSD3

from __future__ import print_function

import matplotlib.pyplot as plt

from specio import specread
from specio.datasets import load_spc_path

print(__doc__)

# Find the path to the SPC toy data
spc_filename = load_spc_path()
print(spc_filename)

# Read the data
spectra = specread(spc_filename)

# Plot the first spectra
plt.plot(spectra.wavelength,
         spectra.amplitudes)
plt.xlabel(spectra.meta['xlabel'])
plt.ylabel(spectra.meta['ylabel'])
plt.show()
