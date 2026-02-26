import pytest
import numpy as np
from numanalysislib.basis._abstract import PolynomialBasis
from numanalysislib.basis.affine import AffinePolynomialBasis


def test_vector_pull_back():
    """
    Test if the interval [-4, 5] is successfully mapped to [-1, 1]
    """
    a_hat = -1
    b_hat = 1

    a = -4
    b = 5

    Affine = AffinePolynomialBasis(hat_a = -1, hat_b = 1, a = -4, b = 5)

    physical_int = np.linspace(a, b, 100)
    reference_int = np.linspace(a_hat, b_hat, 100)

    mapped_physical_int = Affine.pull_back(physical_int)

    np.testing.assert_allclose(mapped_physical_int, reference_int)

def test_vector_push_forward():
    """
    Test if the interval [-1, 1] is successfully mapped to [-4, 5]
    """
    a_hat = -1
    b_hat = 1

    a = -4
    b = 5

    Affine = AffinePolynomialBasis(hat_a = -1, hat_b = 1, a = -4, b = 5)

    physical_int = np.linspace(a, b, 100)
    reference_int = np.linspace(a_hat, b_hat, 100)

    mapped_reference_int = Affine.push_forward(reference_int)

    np.testing.assert_allclose(mapped_reference_int, physical_int)

def test_failure_hats():
    """
    Check for failure
    """
    a_hat = 1
    b_hat = 0

    a = 10
    b = 20
