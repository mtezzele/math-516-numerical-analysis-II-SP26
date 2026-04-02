"""
Goal: Differentiation module for polynomial bases objects. Provides analytical and numerical differentiation 
for any PolynomialBasis object.

Methods: 
- `differentiate(basis, coefficients)`: Returns the PowerBasis Representation and coefficients of the derivative polynomial.
- `evaluate_derivative(basis, coefficients, x)`: Evaluates the derivative at point using central difference method.

Note: For non-PowerBasis objects, we first fit the function to a PowerBasis representation before differentiating. 
"""
import numpy as np
from numanalysislib.basis._abstract import PolynomialBasis
from numanalysislib.basis.power import PowerBasis
from numanalysislib.basis.affine import AffinePolynomialBasis
from typing import Tuple

def differentiate(basis: PolynomialBasis, coefficients: np.ndarray) -> Tuple[PolynomialBasis, np.ndarray]:
    """
    Compute the derivative polynomial analytically.

    For a PowerBasis input, coefficients are differentiated directly. For any other basis, 
    the polynomial is first converted to the PowerBasis via interpolation, then
    differentiated.

    Parameters
    ----------
    basis: PolynomialBasis
        The PolynomialBasis object representing the polynomial.
    coefficients: np.ndarray
        Array of shape (n_dofs,) containing the basis coefficients.

    Returns
    -------
    Tuple[PolynomialBasis, np.ndarray]
        A new PowerBasis of degree n-1 and its coefficients representing the derivative polynomial.
    """
    if basis.degree == 0:
        return PowerBasis(0), np.array([0.0])

    if isinstance(basis, PowerBasis):
        indices = np.arange(1, len(coefficients))
        new_coeffs = indices * coefficients[1:]
        return PowerBasis(basis.degree - 1), new_coeffs

    n = basis.degree
    x_pts = np.linspace(basis.a, basis.b, n + 1)
    y_pts = basis.evaluate(coefficients, x_pts)

    temp_basis = PowerBasis(n)
    temp_coeffs = temp_basis.fit(x_pts, y_pts)

    indices = np.arange(1, len(temp_coeffs))
    new_coeffs = indices * temp_coeffs[1:]

    return PowerBasis(n - 1), new_coeffs

def evaluate_derivative(basis: PolynomialBasis, coefficients: np.ndarray, x: float, h: float = 1e-7) -> np.ndarray:
    """
    Evaluate the derivative numerically via centered differences.
    Computes the approximation p'(x) ≈ (p(x + h) - p(x - h)) / (2h), which is second-order accurate.

    Parameters
    ----------
    basis: PolynomialBasis
        The PolynomialBasis object representing the polynomial.
    coefficients: np.ndarray
        Array of shape (n_dofs,) containing the basis coefficients.
    x: float
        The point at which to evaluate the derivative.
    h: float, optional
        The step size for finite difference (default: 1e-7).

    Returns
    -------
    np.ndarray
        The numerical approximation of the derivative at point x as np.ndarray.
    """
    x = np.asarray(x)
    f_next = basis.evaluate(coefficients, x + h)
    f_prev = basis.evaluate(coefficients, x - h)
    deriv = (f_next - f_prev) / (2 * h)
    return deriv