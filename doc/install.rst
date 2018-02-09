######################
Install and contribute
######################

Dependencies
============

Mandatory dependencies
----------------------

* numpy
* six

Optional dependencies
---------------------

* pandas
* spc
* pyopenms

Install
=======

You can install the dependencies via pip::

  pip install -r requirements.txt

You can install the package using pip and the PyPi repository::

  pip install -U specio

Alternatively, you can clone it and run the setup.py file. Use the following
commands to get a copy from Github and install::

  git clone https://github.com/paris-saclay-cds/specio.git
  cd specio
  pip install .

You can also install the master branch directly with pip::

  pip install git+https://github.com/paris-saclay-cds/specio.git

Test and coverage
=================

You want to test the code before to install::

  $ make test

You wish to test the coverage of your version::

  $ make coverage

Note that `make` is only available in Unix platform.

Contribute
==========

You can contribute to this code through Pull Request on GitHub_. Please, make
sure that your code is coming with unit tests to ensure full coverage and
continuous integration in the API.

.. _GitHub: https://github.com/paris-saclay-cds/specio/pulls
