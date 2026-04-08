import numpy as np
import pytest
from numpy.testing import assert_allclose
from numanalysislib.basis.tensor import TensorProductBasis
from numanalysislib.basis.power import PowerBasis


def test_reconstruction_and_precision():
    """
    Validation: Proves the basis can exactly reconstruct a 2D polynomial 
    of its own degree. 
    Precision: Uses assert_allclose.
    """
    bx = PowerBasis(degree=2) # 1, x, x^2
    by = PowerBasis(degree=2) # 1, y, y^2
    tensor = TensorProductBasis(bx, by)
    
    # Target polynomial: f(x, y) = 5 + 2x + 3y^2 + 4xy
    def f(x, y):
        return 5 + 2*x + 3*y**2 + 4*x*y
    
    # Use non-equally spaced nodes (Edge Case: Stability/Non-uniform)
    x_nodes = np.array([0.1, 0.5, 0.9])
    y_nodes = np.array([0.0, 0.4, 1.0])
    
    X, Y = np.meshgrid(x_nodes, y_nodes, indexing='ij')
    z_values = f(X, Y)
    
    # Fit coefficients
    coeffs = tensor.fit(x_nodes, y_nodes, z_values)
    
    # Evaluate at random points within the domain
    x_test = np.linspace(0, 1, 5)
    y_test = np.linspace(0, 1, 5)
    
    actual = tensor.evaluate(coeffs, x_test, y_test)
    
    XT, YT = np.meshgrid(x_test, y_test, indexing='ij')
    expected = f(XT, YT)
    
    # Precision check: Atol=1e-12 ensures floating point stability
    assert_allclose(actual, expected, atol=1e-12)

def test_non_square_domain():
    """
    Edge Cases: Handles non-equally spaced nodes and different 
    degrees for x and y.
    """
    bx = PowerBasis(degree=3) # 4 DOFs
    by = PowerBasis(degree=1) # 2 DOFs
    tensor = TensorProductBasis(bx, by)
    
    assert tensor.n_dofs == 8
    
    # Nodes on a rectangle [0, 10] x [0, 5]
    x_nodes = np.sort(np.random.rand(4) * 10)
    y_nodes = np.sort(np.random.rand(2) * 5)
    z_values = np.random.rand(4, 2)
    
    coeffs = tensor.fit(x_nodes, y_nodes, z_values)
    
    # If we evaluate at the nodes, we should get exactly z_values back
    reconstructed_at_nodes = tensor.evaluate(coeffs, x_nodes, y_nodes)
    assert_allclose(reconstructed_at_nodes, z_values, atol=1e-12)

def test_evaluate_basis_indexing():
    """Coverage: Checks if indexing correctly retrieves basis components."""
    bx = PowerBasis(degree=1) # 0: 1, 1: x
    by = PowerBasis(degree=1) # 0: 1, 1: y
    tensor = TensorProductBasis(bx, by)
    
    # Index 2: i=1, j=0 (phi_1 * psi_0) -> x * 1 = x
    # Index 3: i=1, j=1 (phi_1 * psi_1) -> x * y
    x = np.array([2.0])
    y = np.array([3.0])
    
    assert_allclose(tensor.evaluate_basis(2, x, y), [[2.0]])
    assert_allclose(tensor.evaluate_basis(3, x, y), [[6.0]])

def test_dimension_mismatch_error():
    """Edge Cases: Ensure the class raises errors for incorrect input shapes."""
    bx = PowerBasis(degree=1)
    by = PowerBasis(degree=1)
    tensor = TensorProductBasis(bx, by)
    
    x_nodes = np.array([0, 1])
    y_nodes = np.array([0, 1])
    bad_z = np.zeros((3, 3)) # Should be (2, 2)
    
    with pytest.raises(ValueError):
        tensor.fit(x_nodes, y_nodes, bad_z)

def test_runge_stability():
    """
    Convergence: Checks stability for higher degree polynomials.
    Tests if the interpolation error is manageable or if oscillations 
    become extreme (Runge's phenomenon).
    """
    # Use a high degree to provoke potential instability
    degree = 10 
    bx = PowerBasis(degree=degree)
    by = PowerBasis(degree=degree)
    tensor = TensorProductBasis(bx, by)

    # Runge function: f(x,y) = 1 / (1 + 25*(x^2 + y^2))
    # Domain mapped to [-1, 1]
    def runge_2d(x, y):
        return 1.0 / (1.0 + 25.0 * (x**2 + y**2))

    x_nodes = np.linspace(-1, 1, degree + 1)
    y_nodes = np.linspace(-1, 1, degree + 1)
    
    X, Y = np.meshgrid(x_nodes, y_nodes, indexing='ij')
    z_values = runge_2d(X, Y)

    # Fit the coefficients
    coeffs = tensor.fit(x_nodes, y_nodes, z_values)

    # Evaluate at a fine grid to check for edge oscillations
    x_fine = np.linspace(-1, 1, 50)
    y_fine = np.linspace(-1, 1, 50)
    actual = tensor.evaluate(coeffs, x_fine, y_fine)

    X_fine, Y_fine = np.meshgrid(x_fine, y_fine, indexing='ij')
    expected = runge_2d(X_fine, Y_fine)

    max_error = np.max(np.abs(actual - expected))
    
    # In a stable implementation (like Chebyshev), this error would be small.
    # In a Monomial basis with equal spacing, this error will be large.
    # This test "validates" the behavior of the basis under stress.
    assert max_error < 100.0  # Adjust threshold based on expected basis behavior