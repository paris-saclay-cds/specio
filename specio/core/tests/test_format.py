"""Test the format class."""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import gc
import shutil
from tempfile import mkdtemp
from os.path import dirname, join

import numpy as np

from pytest import raises

from specio import formats
from specio.core import Format, Request, FormatManager
from specio.plugins.example import DummyFormat
from specio.testing import assert_raises_regex

DATA_PATH = module_path = dirname(__file__)


class MyFormat(Format):
    """ TEST DOCS """
    _closed = []

    def _can_read(self, request):
        return request.filename.lower().endswith(self.extensions + ('.haha', ))

    class Reader(Format.Reader):
        _failmode = False

        def _open(self):
            self._read_frames = 0

        def _close(self):
            self.format._closed.append(id(self))

        def _get_length(self):
            return 3

        def _get_data(self, index):
            if self._failmode == 2:
                raise IndexError()
            elif self._failmode:
                return 'not an array', {}
            else:
                self._read_frames += 1
                return (np.ones((10, 10)) * index,
                        np.ones((10,)) * index,
                        self._get_meta_data(index))

        def _get_meta_data(self, index):
            if self._failmode:
                return 'not a dict'
            return {'index': index}


def test_format():
    F = Format('testname', 'test description', 'foo bar spam')
    assert F.name == 'TESTNAME'
    assert F.description == 'test description'
    assert F.name in repr(F)
    assert F.name in F.doc
    assert str(F) == F.doc
    assert set(F.extensions) == set(['.foo', '.bar', '.spam'])

    F1 = Format('test', '', 'foo bar spam')
    F2 = Format('test', '', 'foo, bar,spam')
    F3 = Format('test', '', ['foo', 'bar', 'spam'])
    F4 = Format('test', '', '.foo .bar .spam')
    for F in (F1, F2, F3, F4):
        assert set(F.extensions) == set(['.foo', '.bar', '.spam'])
    # Fail
    assert_raises_regex(ValueError, "Invalid value for extensions given.",
                        Format, 'test', '', 3)


def test_format_subclass():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    F = MyFormat('test', '')
    assert 'TEST DOCS' in F.doc

    # Get and check reader and write classes
    R = F.get_reader(Request(filename))
    assert isinstance(R, MyFormat.Reader)
    assert R.format is F
    assert R.request.filename == filename


def test_format_context_manager():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    F = MyFormat('test', '')
    R = F.get_reader(Request(filename))
    # Use as context manager
    with R:
        pass
    # Objects are now closed, cannot be used
    assert R.closed
    assert_raises_regex(RuntimeError, "I/O operation on closed Reader.",
                        R.__enter__)
    assert_raises_regex(RuntimeError, "I/O operation on closed Reader.",
                        R.get_data, 0)

    R = F.get_reader(Request(filename))
    ids = id(R)
    F._closed[:] = []
    del R
    gc.collect()  # Invoke __del__
    assert ids == F._closed[0]


def test_reader():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    F = MyFormat('test', '')

    # Test using reader
    n = 3
    R = F.get_reader(Request(filename))
    assert len(R) == n
    specs = [spec for spec in R]
    assert len(specs) == n
    for i in range(3):
        assert specs[i].spectrum[0, 0] == i
        assert specs[i].wavelength[0] == i
        assert specs[i].meta['index'] == i
    for i in range(3):
        assert R.get_meta_data(i)['index'] == i
    # Read next
    assert R.get_data(0).spectrum[0, 0] == 0
    assert R.get_next_data().spectrum[0, 0] == 1
    assert R.get_next_data().spectrum[0, 0] == 2
    # Fail
    R._failmode = 1
    assert_raises_regex(ValueError, "unpack",
                        R.get_data, 0)
    assert_raises_regex(ValueError, "Meta data must be a dict,",
                        R.get_meta_data, 0)
    R._failmode = 2
    with raises(IndexError):
        [spec for spec in R]


def test_default_can_read():
    F = DummyFormat('test', '', 'foobar')

    # Prepare files
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    filename_wrong_ext = join(DATA_PATH, 'data', 'spectra.notavalidext')

    # Test _can_read()
    assert F.can_read(Request(filename))
    assert not F.can_read(Request(filename_wrong_ext))


def test_format_selection():
    filename = join(DATA_PATH, 'data', 'spectra.foobar')
    test_dir = mkdtemp()
    fname2 = join(test_dir, 'test.selectext1')
    fname3 = join(test_dir, 'test.haha')
    open(fname2, 'wb')
    open(fname3, 'wb')

    try:
        F = formats.search_read_format(Request(filename))
        assert F is formats['DUMMY']

        # Now with custom format
        format = MyFormat('test_selection', 'xx', 'selectext1')
        formats.add_format(format)
        assert '.selectext1' in fname2
        F = formats.search_read_format(Request(fname2))
        assert F is format
        assert '.haha' in fname3
        F = formats.search_read_format(Request(fname3))
        assert F is format
    finally:
        shutil.rmtree(test_dir)


def test_format_manager():
    assert isinstance(formats, FormatManager)
    assert len(formats) > 0
    assert 'FormatManager' in repr(formats)
    smalldocs = str(formats)
    for format in formats:
        assert isinstance(format, Format)
        assert format.name in smalldocs

    F1 = formats['FOOBAR']
    F2 = formats['.foobar']
    assert F1 is F2
    assert_raises_regex(ValueError, "Looking up a format should be done by",
                        formats.__getitem__, 678)
    assert_raises_regex(IndexError,
                        "No format known by name .nonexistentformat",
                        formats.__getitem__, '.nonexistentformat')

    myformat = Format('test', 'test description', 'testext1 testext2')
    formats.add_format(myformat)
    assert myformat in [f for f in formats]
    assert formats['testext1'] is myformat
    assert formats['testext2'] is myformat
    assert_raises_regex(ValueError,
                        "add_format needs argument to be a Format object",
                        formats.add_format, 678)
    assert_raises_regex(ValueError,
                        "Given Format instance is already registered",
                        formats.add_format, myformat)

    myformat2 = Format('test', 'other description', 'foobar')
    assert_raises_regex(ValueError,
                        "A Format named 'TEST' is already registered",
                        formats.add_format, myformat2)
    formats.add_format(myformat2, True)  # overwrite
    assert formats['test'] is not myformat
    assert formats['test'] is myformat2

    assert_raises_regex(ValueError, "No format matches the empty string",
                        formats.__getitem__, '')

    formats.show()


def test_sorting_errors():
    assert_raises_regex(TypeError, "accepts only string names.",
                        formats.sort, 3)
    assert_raises_regex(ValueError,
                        "should not contain dots or commas.",
                        formats.sort, 'foo, bar')
    assert_raises_regex(ValueError,
                        "should not contain dots or commas.",
                        formats.sort, 'foo.png')
