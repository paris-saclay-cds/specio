"""
===================================
Read SP Perkin Elmer IR binary file
===================================

This example shows how to read SP file and plot the results.

"""

# Authors: Guillaume Lemaitre <guillaume.lemaire@inria.fr>
# License: BSD3

from __future__ import print_function

import matplotlib.pyplot as plt

from specio import specread
from specio.datasets import load_sp_path

print(__doc__)

# Find the path to the SP toy data
sp_filename = load_sp_path()
print(sp_filename)

# Read the data
spectra = specread(sp_filename)

# Plot the first spectra
plt.plot(spectra.wavelength,
         spectra.amplitudes)
plt.show()
