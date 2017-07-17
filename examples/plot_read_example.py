"""
===============
General example
===============

This is a general example presenting how to read a spectra file.

"""
from __future__ import print_function
from os.path import join
from specio import specread

print(__doc__)

filename = join('data', 'spectra.foobar')
spec = specread(filename)
print(spec)
