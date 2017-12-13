"""
====================================================
Read SPC Galactic Industries Corporation binary file
====================================================

This example shows how to read SPC file and plot the results.

"""

from __future__ import print_function

import matplotlib.pyplot as plt

from specio import specread
from specio.datasets import load_spc_path

# Find the path to the SPC toy data
spc_filename = load_spc_path()
print(spc_filename)

# Read the data
spectra = specread(spc_filename)

# Plot the first spectra
plt.plot(spectra.wavelength,
         spectra.spectrum)
plt.xlabel(spectra.meta['xlabel'])
plt.ylabel(spectra.meta['ylabel'])
plt.show()
