#!/bin/bash
# This script is meant to be called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.

# License: 3-clause BSD

# Travis clone pydicom/pydicom repository in to a local repository.

set -e

echo 'List files from cached directories'
echo 'pip:'
ls $HOME/.cache/pip


# Deactivate the travis-provided virtual environment and setup a
# conda-based environment instead
deactivate

# Install miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
     -O miniconda.sh
MINICONDA_PATH=/home/travis/miniconda
chmod +x miniconda.sh && ./miniconda.sh -b -p $MINICONDA_PATH
export PATH=$MINICONDA_PATH/bin:$PATH
conda update --yes conda

# Configure the conda environment and put it in the path using the
# provided versions
conda create -n testenv --yes python=$PYTHON_VERSION pip
source activate testenv
conda install --yes numpy pandas six pytest pytest-cov pytest-mock
pip install codecov

# install spc dependency from master
pip install git+https://github.com/glemaitre/spc.git
pip install pyopenms

python --version
python -c "import numpy; print('numpy %s' % numpy.__version__)"
cd $TRAVIS_BUILD_DIR
pip install -e .
