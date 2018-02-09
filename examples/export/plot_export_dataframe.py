"""
==============================================
Export a specio.Spectrum to a pandas.DataFrame
==============================================

This example illustrates how to export a spectrum into a dataframe which can be
useful for some later processing.

"""

# Authors: Guillaume Lemaitre <guillaume.lemaire@inria.fr>
# License: BSD3

import matplotlib.pyplot as plt

from specio.datasets import load_csv_path
from specio import specread

# read the spectrum
spectra = specread(load_csv_path())

# convert to a dataframe
df_spectra = spectra.to_dataframe()

# print the head of dataframe
print(df_spectra.head())

# plot the five first spectra
df_spectra.head().T.plot()

# or on different plots
df_spectra.head().T.plot(subplots=True)

plt.show()
