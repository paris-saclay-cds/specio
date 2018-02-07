import os
import sys
import glob
from tempfile import mkdtemp
from shutil import rmtree

import pytest

from numpy.testing import assert_allclose
from numpy.testing import assert_array_equal

from specio import specread

# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separate installable pytest-cli plugin.
pytest_plugins = ["pytester"]

module_data_path = os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def run(testdir):
    def do_run(*args):
        args = ["specio"] + list(args)
        return testdir._run(*args)
    return do_run


@pytest.mark.parametrize(
    "filename_input, filename_output",
    [(os.path.join(module_data_path, 'sp1.spc'), None),
     (os.path.join(module_data_path, 'sp1.spc'), 'spectra.csv'),
     (os.path.join(module_data_path, '*.spc'), 'spectra.csv'),
     (os.path.join(module_data_path, '*.spc'), None)])
def test_specio_cli_single_spectrum(filename_input, filename_output, run):
    # test when specread return a Spectrum instance
    tmp_dir = mkdtemp()
    try:
        if filename_output is None:
            run("convert", filename_input)
            basename, _ = os.path.splitext(
                sorted(glob.glob(filename_input))[0])
            filename_output = basename + '.csv'
        else:
            filename_output = os.path.join(tmp_dir, filename_output)
            run("convert", filename_input, '-o', filename_output)

        assert os.path.isfile(filename_output)

        spectra_original = specread(filename_input).to_dataframe()
        spectra_exported = specread(filename_output).to_dataframe()

        assert_allclose(spectra_original.values, spectra_exported.values)
        assert_allclose(spectra_original.columns.values,
                        spectra_exported.columns.values)
        assert_array_equal(spectra_original.index.values,
                           spectra_exported.index.values)
    finally:
        rmtree(tmp_dir)
        if os.path.isfile(filename_output):
            os.remove(filename_output)


@pytest.mark.skipif(
    (sys.platform == 'win32') and (sys.version_info < (3, 5)),
    reason="OpenMS not available")
@pytest.mark.parametrize(
    "filename_input, filename_output",
    [(os.path.join(module_data_path, 'spectra.mzml'), None),
     (os.path.join(module_data_path, 'spectra.mzml'), 'spectra')])
def test_specio_cli_multi_spectra(filename_input, filename_output, run,
                                  testdir):
    # test when specread return a list of Spectrum instance
    tmp_dir = mkdtemp()
    try:
        if filename_output is None:
            run("convert", filename_input)
            output_folder = testdir.tmpdir.__str__()
        else:
            filename_output = os.path.join(tmp_dir, filename_output)
            run("convert", filename_input, '-o', filename_output)
            output_folder = tmp_dir

        exported_files = glob.glob(os.path.join(output_folder, '*.csv'))
        assert len(exported_files) == 531

    finally:
        rmtree(tmp_dir)
