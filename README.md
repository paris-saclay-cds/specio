# specio: Python input/output for spectroscopic files

[![Build Status](https://travis-ci.org/paris-saclay-cds/specio.svg?branch=master)](https://travis-ci.org/paris-saclay-cds/specio)
[![Build status](https://ci.appveyor.com/api/projects/status/pvkh4hic8rpxcoyn?svg=true)](https://ci.appveyor.com/project/glemaitre/specio-crk9i)
[![Documentation Status](https://readthedocs.org/projects/specio/badge/?version=latest)](http://specio.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/paris-saclay-cds/specio/branch/master/graph/badge.svg)](https://codecov.io/gh/paris-saclay-cds/specio)


`specio` is a library which allows to easily open spectroscopic format
currently available. It is widely inspired by
the [`imageio`](https://github.com/imageio/imageio) architecture.

## Dependencies

### Mandatory dependencies

* numpy
* six

### Optional dependencies

#### Export

* pandas

#### Reader

* spc
* pyopenms
