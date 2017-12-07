"""Test the Request class"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import shutil
import os
from os.path import dirname, join, sep, expanduser

import pytest
from pytest import raises

from specio import core
from specio.core import Request

DATA_PATH = module_path = dirname(__file__)


class File():
    def read(self, n):
        return b'\x00' * n

    def seek(self, i):
        raise IOError('Not supported')

    def tell(self):
        raise Exception('Not supported')

    def close(self):
        pass


def test_request():
    filename = 'file://' + join(DATA_PATH, 'data', 'spectra.foobar')
    R = Request(filename)
    assert R._uri_type == core.request.URI_FILENAME
    assert R.get_local_filename() == filename[7:]
    file_obj = R.get_file()
    assert file_obj.name == filename[7:]

    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R = Request(filename)
    assert R._uri_type == core.request.URI_FILENAME
    assert R.get_local_filename() == filename
    file_obj = R.get_file()
    assert file_obj.name == filename

    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    file_obj = open(filename, 'rb')
    R = Request(file_obj)
    assert R.get_local_filename() == filename
    assert R.get_file().name == filename

    shutil.copy(filename, expanduser('~/'))
    filename = '~/spectra.foobar'
    R = Request(filename)
    assert R.filename == expanduser('~/spectra.foobar').replace('/', sep)
    os.remove(expanduser(filename))
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R = Request(filename, some_kwarg='something')
    assert R.kwargs == {'some_kwarg': 'something'}


@pytest.mark.parametrize(
    'type_error,msg,params',
    [(IOError, "Cannot understand given URI", ['invalid', 'uri'] * 10),
     (IOError, "Cannot understand given URI", 4),
     (IOError, "No such file", '/does/not/exist'),
     (IOError, "No such file", '/does/not/exist.zip/spam.png')])
def test_request_error(type_error, msg, params):
    with pytest.raises(type_error, message=msg):
        Request(params)


def test_request_read_sources():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R = Request(filename)
    first_bytes = R.firstbytes
    all_bytes = open(filename, 'rb').read()
    assert len(first_bytes) == 256
    assert all_bytes.startswith(first_bytes)


def test_request_file_no_seek():
    R = Request(File())
    with raises(IOError):
        R.firstbytes
