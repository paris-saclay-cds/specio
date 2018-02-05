"""
======================================
Read CSV Comma-separated values format
======================================

This example shows how to read CSV file and plot the results. Note that this
format is the format used when using :func:`specio.core.Spectrum.to_csv`

"""

# Authors: Guillaume Lemaitre <guillaume.lemaire@inria.fr>
# License: BSD3

from __future__ import print_function

import matplotlib.pyplot as plt

from specio import specread
from specio.datasets import load_csv_path

print(__doc__)

# Find the path to the CSV toy data
csv_filename = load_csv_path()
print(csv_filename)

# Read the data
spectra = specread(csv_filename)

# Plot the first spectra
plt.plot(spectra.wavelength,
         spectra.amplitudes.T)
plt.xlabel('Amplitude')
plt.ylabel('Wavelength')
plt.show()
