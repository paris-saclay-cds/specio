"""
==============================================
Read FSM Perkin Elmer Spotlight IR binary file
==============================================

This example shows how to read FSM file and plot the results.

"""

# Authors: Guillaume Lemaitre <guillaume.lemaire@inria.fr>
# License: BSD3

from __future__ import print_function

import matplotlib.pyplot as plt

from specio import specread
from specio.datasets import load_fsm_path

print(__doc__)

# Find the path to the FSM toy data
fsm_filename = load_fsm_path()
print(fsm_filename)

# Read the data
spectra = specread(fsm_filename)

# Plot the first spectra
plt.plot(spectra.wavelength,
         spectra.amplitudes[0])
plt.show()
