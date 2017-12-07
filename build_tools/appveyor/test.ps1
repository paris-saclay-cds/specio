# Change to a non-source folder to make sure we run the tests on the
# installed library.
- "cd C:\\"

$installed_specio_folder = $(python -c "import os; os.chdir('c:/'); import specio;\
print(os.path.dirname(specio.__file__))")
echo "specio found in: $installed_specio_folder"

# --pyargs argument is used to make sure we run the tests on the
# installed package rather than on the local folder
py.test --pyargs specio $installed_specio_folder
exit $LastExitCode
