import numpy as np
from numanalysislib.basis._abstract import PolynomialBasis

class TensorProductBasis(PolynomialBasis):
    def __init__(self, bx: PolynomialBasis, by: PolynomialBasis):
        self.bx = bx
        self.by = by
        self.nx = bx.n_dofs
        self.ny = by.n_dofs
        super().__init__(self.nx * self.ny)

    def _unflatten_index(self, index: int):
        """Helper function to loop through vectors"""
        return divmod(index, self.ny)

    def evaluate_basis(self, index: int, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        if index < 0 or index >= self.n_dofs:
            raise ValueError(f"Basis index {index} out of range")
        
        i, j = self._unflatten_index(index)
        
        phi_i = self.bx.evaluate_basis(i, x)
        psi_j = self.by.evaluate_basis(j, y)
        
        return np.outer(phi_i, psi_j)

    def evaluate(self, coefficients: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        if coefficients.size != self.n_dofs:
            raise ValueError(f"Expected {self.n_dofs} coefficients, got {coefficients.size}")
        
        res = np.zeros((len(x), len(y)))
        
        coeffs_2d = coefficients.reshape((self.nx, self.ny))
        
        for i in range(self.nx):
            for j in range(self.ny):
                c = coeffs_2d[i, j]
                if c != 0:
                    res += c * self.evaluate_basis(i * self.ny + j, x, y)
        return res

    def fit(self, x_nodes: np.ndarray, y_nodes: np.ndarray, z_values: np.ndarray) -> np.ndarray:
        """
        Computes 2D coefficients given grid nodes and the target values at those nodes.
        z_values should be a 2D array of shape (len(x_nodes), len(y_nodes)).
        """
        x_nodes = np.asarray(x_nodes)
        y_nodes = np.asarray(y_nodes)
        z_values = np.asarray(z_values)

        if z_values.shape != (len(x_nodes), len(y_nodes)):
            raise ValueError(f"z_values shape {z_values.shape} must match nodes grid.")

        intermediate_coeffs = np.zeros((self.nx, len(y_nodes)))
        for j in range(len(y_nodes)):
            intermediate_coeffs[:, j] = self.bx.fit(x_nodes, z_values[:, j])

        final_coeffs_matrix = np.zeros((self.nx, self.ny))
        for i in range(self.nx):
            final_coeffs_matrix[i, :] = self.by.fit(y_nodes, intermediate_coeffs[i, :])

        return final_coeffs_matrix