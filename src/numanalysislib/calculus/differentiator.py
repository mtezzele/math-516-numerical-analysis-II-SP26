"""
Goal: Differentiation module for polynomial bases objects. Provides analytical and numerical differentiation 
for any PolynomialBasis object.

Methods: 
- `differentiate(basis, coefficients)`: Returns the PowerBasis Representation and coefficients of the derivative polynomial.
- `evaluate_derivative(basis, coefficients, x)`: Evaluates the derivative at point using central difference method.

Note: For non-PowerBasis objects, we first fit the function to a PowerBasis representation before differentiating. 
"""
import numpy as np
import math
from numanalysislib.basis._abstract import PolynomialBasis
from numanalysislib.basis.power import PowerBasis
from numanalysislib.basis.affine import AffinePolynomialBasis
from typing import Tuple

def differentiate(basis: PolynomialBasis, coefficients: np.ndarray, k: int = 1) -> Tuple[PolynomialBasis, np.ndarray]:
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
    k: int, optional
        The order of the derivative to compute (default: 1).

    Returns
    -------
    Tuple[PowerBasis, np.ndarray]
        A new PowerBasis of degree n-1 and its coefficients representing the derivative polynomial.
    """
    for _ in range(k):
        if isinstance(basis, PowerBasis):
            basis, coefficients = basis.differentiate_coefficients(coefficients)
        else:
            # For non-PowerBasis, fit to PowerBasis first, then differentiate
            n = basis.degree
            x_pts = np.linspace(basis.a, basis.b, n + 1)
            y_pts = basis.evaluate(coefficients, x_pts)
            temp_basis = PowerBasis(n)
            temp_coeffs = temp_basis.fit(x_pts, y_pts)

            basis, coefficients = temp_basis.differentiate_coefficients(temp_coeffs)

    return basis, coefficients

def evaluate_derivative(basis: PolynomialBasis, coefficients: np.ndarray, x: float, k: int =1, h: float = 1e-5, scheme: str = "centered") -> np.ndarray:
    """
    Evaluate the k-th derivative numerically using finite differences via The Taylor Table / Undetermined Coeffiecients approach.
    
    Builds the Taylor table A where A[i, j] = s_i^j / j!,
    solves A^T c = e_k for the weights c, then computes
    f^{(k)}(x) = c^T f / h^k.

    Parameters
    ----------
    basis: PolynomialBasis
        The PolynomialBasis object representing the polynomial.
    coefficients: np.ndarray
        Array of shape (n_dofs,) containing the basis coefficients.
    x: float
        The point at which to evaluate the derivative.
    k: int, optional
        The order of the derivative to compute (default: 1).
    h: float, optional
        The step size for finite difference (default: 1e-5).
    scheme: str, optional
        The finite difference scheme to use: "forward", "backward", or "centered"

    Returns
    -------
    np.ndarray
        The numerical approximation of the k-th derivative at point x as np.ndarray.
    """
    x = np.asarray(x, dtype=float)

    if scheme == "centered":
        s = np.arange(-k, k + 1)
    elif scheme == "forward":
        s = np.arange(0, k + 1)
    elif scheme == "backward":
        s = np.arange(-k, 1)
    else:
        raise ValueError(f"Unknown scheme: {scheme}. Use 'centered', 'forward', or 'backward'.")
    n = len(s)

    # Build Taylor table: A[i, j] = s_i^j / j!
    A = np.zeros((n, n))
    for j in range(n):
        A[:, j] = s**j / math.factorial(j)

    # Solve A^T c = e_k
    e_k = np.zeros(n)
    e_k[k] = 1.0
    c = np.linalg.solve(A.T, e_k)

    # f^{(k)}(x) = c^T f / h^k
    result = np.zeros_like(x, dtype=float)
    for j in range(n):
        result += c[j] * basis.evaluate(
            coefficients, x + s[j] * h
        )

    return result / (h ** k)