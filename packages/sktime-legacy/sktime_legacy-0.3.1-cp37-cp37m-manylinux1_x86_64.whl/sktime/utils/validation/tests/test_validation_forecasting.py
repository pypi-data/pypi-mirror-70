from pytest import raises
import pytest
import numpy as np
from numpy.testing import assert_array_equal
from sktime.utils.validation.forecasting import validate_fh

__author__ = ["Markus Löning"]


bad_input_args = ((1, 2), [], np.array([]),
                  'str', 0.1, [0.1, 0.2], True, [True, False])


@pytest.mark.parametrize("arg", bad_input_args)
def test_validate_fh_bad_input_args(arg):
    with raises(ValueError):
        validate_fh(arg)


