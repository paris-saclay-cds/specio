"""Testing utilities to use pytest"""

# Copyright (c) 2017
# Authors: Guillaume Lemaitre <guillaume.lemaitre@inria.fr>
# License: BSD 3 clause

import pytest


def assert_raises_regex(type_error, message, func, *args, **kwargs):
    with pytest.raises(type_error) as excinfo:
        func(*args, **kwargs)
    excinfo.match(message)
