"""Test the Request class"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import shutil
import os
from os.path import dirname, join, sep, expanduser

from pytest import raises

from specio import core
from specio.core import Request
from specio.testing import assert_raises_regex

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
    R = Request(filename, 's')
    assert R._uri_type == core.request.URI_FILENAME
    assert R.mode == 's'
    assert R.get_local_filename() == filename[7:]
    file_obj = R.get_file()
    assert file_obj.name == filename[7:]

    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R = Request(filename, 's')
    assert R._uri_type == core.request.URI_FILENAME
    assert R.mode == 's'
    assert R.get_local_filename() == filename
    file_obj = R.get_file()
    assert file_obj.name == filename

    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    file_obj = open(filename, 'rb')
    R = Request(file_obj, 's')
    assert R.get_local_filename() == filename
    assert R.get_file().name == filename

    shutil.copy(filename, expanduser('~/'))
    filename = '~/spectra.foobar'
    R = Request(filename, 's')
    assert R.filename == expanduser('~/spectra.foobar').replace('/', sep)
    assert R.mode == 's'
    os.remove(expanduser(filename))
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R = Request(filename, 's', some_kwarg='something')
    assert R.kwargs == {'some_kwarg': 'something'}


def test_request_error():
    assert_raises_regex(ValueError, 'mode must be a string', Request,
                        '/some/file', None)
    assert_raises_regex(ValueError, 'mode must be a string', Request,
                        '/some/file', 3)
    assert_raises_regex(ValueError, 'mode to have one char', Request,
                        '/some/file', '')
    assert_raises_regex(ValueError, 'mode to have one char', Request,
                        '/some/file', 'ss')
    assert_raises_regex(ValueError, 'mode to have one char', Request,
                        '/some/file', 'rii')
    assert_raises_regex(ValueError, 'sS?', Request,
                        '/some/file', 'r')
    assert_raises_regex(IOError, "Cannot understand given URI", Request,
                        ['invalid', 'uri'] * 10, 's')
    assert_raises_regex(IOError, "Cannot understand given URI", Request, 4,
                        's')
    assert_raises_regex(IOError, "No such file", Request,
                        '/does/not/exist', 's')
    assert_raises_regex(IOError, "No such file", Request,
                        '/does/not/exist.zip/spam.png', 's')


def test_request_read_sources():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    R = Request(filename, 's')
    first_bytes = R.firstbytes
    all_bytes = open(filename, 'rb').read()
    assert len(first_bytes) == 256
    assert all_bytes.startswith(first_bytes)


def test_request_file_no_seek():
    R = Request(File(), 's')
    with raises(IOError):
        R.firstbytes
