"""
=========================================
Read proprietary format and export to CSV
=========================================

This example illustrates how to read some proprietary format and export the
resulting spectrum into an internal CSV format. The exported CSV can also be
read using :func:`specio.specread`.

"""

# Authors: Guillaume Lemaitre <guillaume.lemaire@inria.fr>
# License: BSD3

from __future__ import print_function

import os
import sys

import matplotlib.pyplot as plt

from specio import specread

print(__doc__)

# Get the path to the data relatively to this example
DATA_PATH = os.path.dirname(sys.argv[0])

spc_filenames = os.path.join(DATA_PATH, 'data', '*.spc')
print('The SPC files will be search in: {}'.format(spc_filenames))

# Read the data
spectra = specread(spc_filenames)

# Plot the first spectra
plt.figure()
plt.plot(spectra.wavelength,
         spectra.amplitudes.T)

# We get the axis information by using the meta data of the first file read.
plt.xlabel(spectra.meta[0]['xlabel'])
plt.ylabel(spectra.meta[0]['ylabel'])
plt.title('Spectra extracted from the SPC files')

# Export all spectrum into csv
spectra.to_csv('spectra.csv')

# We can open the exported file
spectra_csv = specread('spectra.csv')

# Plot the first spectra
plt.figure()
plt.plot(spectra_csv.wavelength,
         spectra_csv.amplitudes.T)

# We get the axis information by using the meta data of the first file read.
plt.xlabel('Amplitudes')
plt.ylabel('Wavelength')
plt.title('Spectra extracted from the CSV files')

plt.show()
