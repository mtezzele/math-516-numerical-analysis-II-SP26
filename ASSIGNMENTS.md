# Assignments

## 📚 Overview of Student Assignments

This repository is a collaborative project. Each student is assigned a specific module to implement, document, and test. By the end of the semester, these modules will work together to solve complex numerical problems.

**General Requirements:**
- **Inheritance:** Your class must inherit from `PolynomialBasis`.
- **Vectorization:** Use `numpy` operations; avoid Python `for` loops for mathematical evaluations.
- **Testing:** Provide a test file in `tests/` verifying your code against analytical solutions.
- **Type Hinting:** Use Python type hints for all method signatures.

---

## 🏗️ Group 1: Core Infrastructure

### Task 1: The Affine Mapper (`AffinePolynomialBasis`)
**Module:** `src/numanalysislib/basis/affine.py`

**Goal:** Handle the mapping between a "Reference Interval" (e.g., $[-1, 1]$) and a "Physical Interval" $[a, b]$.

- **Methods:** 
  - `pull_back(x)`: Maps $x \in [a, b] \to \hat{x} \in [\hat{a}, \hat{b}]$.
  - `push_forward(hat_x)`: Maps $\hat{x} \in [\hat{a}, \hat{b}] \to x \in [a, b]$.
- **Math:** $x = a + \frac{\hat{x} - \hat{a}}{\hat{b} - \hat{a}}(b - a)$.
- **Note:** All other basis implementations will inherit from this class to gain domain-flexibility.

---

## 📐 Group 2: Polynomial Implementations
*All implementations must inherit from `PolynomialBasis`.*

### Task 2: The Power Basis (`PowerBasis`)
**Module:** `src/numanalysislib/basis/power.py`
- **Definition:** Basis $1, x, x^2, \dots, x^n$.
- **Fit:** Construct the **Vandermonde Matrix** and solve $Vc = y$.
- **Challenge:** Monitor the condition number of the matrix.

### Task 3: The Lagrange Basis (`LagrangePolynomial`)
**Module:** `src/numanalysislib/basis/lagrange.py`
- **Definition:** $L_i(x) = \prod_{j \neq i} \frac{x - x_j}{x_i - x_j}$.
- **Fit:** Trivial (coefficients are the function values).
- **Evaluation:** Implement the **Barycentric Formula** for numerical stability.

### Task 4: The Newton Basis (`NewtonPolynomial`)
**Module:** `src/numanalysislib/basis/newton.py`
- **Definition:** $n_i(x) = \prod_{j=0}^{i-1} (x - x_j)$.
- **Fit:** Implement the **Divided Differences** algorithm.
- **Evaluation:** Implement **Horner’s Scheme** for efficiency.

### Task 5: The Bernstein Basis (`BernsteinPolynomial`)
**Module:** `src/numanalysislib/basis/bernstein.py`
- **Definition:** $B_{i,n}(x) = \binom{n}{i} x^i (1-x)^{n-i}$ on $[0, 1]$.
- **Fit:** Solve the linear system $Ac = y$ to force interpolation.
- **Bonus:** Implement a Bezier approximation method.

### Task 6: The Chebyshev Basis (`ChebyshevPolynomial`)
**Module:** `src/numanalysislib/basis/chebyshev.py`
- **Definition:** $T_n(x) = \cos(n \arccos x)$ on $[-1, 1]$.
- **Nodes:** Implement a helper to return **Chebyshev Nodes** (roots/extrema).
- **Note:** Map the optimal nodes from $[-1, 1]$ to $[a, b]$ using the parent class. Be sure it works with `AffinePolynomialBasis`.

### Task 7: The Hermite Basis (`HermitePolynomial`)
**Module:** `src/numanalysislib/basis/hermite.py`
- **Definition:** Cubic polynomials using values AND derivatives at endpoints.
- **Fit:** Accepts a vector $[v_a, d_a, v_b, d_b]$.
- **Note:** Account for the Jacobian $1/(b-a)$ when mapping derivatives from the reference to the physical domain. Be sure it works with `AffinePolynomialBasis`.

---

## 🔗 Group 3: Composite & High-Dimensional Structures

### Task 8: Continuous Piecewise Manager (`PiecewisePolynomial`)
**Module:** `src/numanalysislib/basis/piecewise.py`
- **Goal:** Create a global continuous function by stitching basis objects over a mesh. A class that takes a type of basis (e.g., `LagrangePolynomial) and a mesh (list of intervals), creating a global continuous function.
- **Continuity:** The "last" node of element $k$ is the "first" node of element $k+1$.
- **Evaluation:** Given $x$, find which element it belongs to (binary search for example), and delegate to that element's `evaluate method.

### Task 9: Discontinuous Galerkin Basis (`BrokenPolynomial`)
**Module:** `src/numanalysislib/basis/broken.py`
- **Goal:** Manage piecewise polynomials with no continuity constraints at interfaces. Similar to Task 8, but enforces no continuity between elements. This is the basis for Discontinuous Galerkin (DG) methods.
- **Difference:** It does not share nodes at interfaces. If the mesh has $N$ elements and degree $k$, there are $N(k+1)$ degrees of freedom.
- **L2 Projection:** Implement local mass matrix inversion to project a function onto the broken space.

### Task 10: 2D Tensor Product (`TensorProductBasis`)
**Module:** `src/numanalysislib/basis/tensor.py`
- **Goal:** Constructs a 2D basis on a rectangle $[x_a, x_b] \times [y_a, y_b]$ given two 1D basis objects, $B_x$ and $B_y$.
- **Definition:** $\Phi_{ij}(x, y) = \phi_i(x) \cdot \psi_j(y)$.
- **Differences:** `evaluate` and `fit` will now take 2D arrays.

---

## ⚙️ Group 4: Operators & Utilities

### Task 11: Integration Engine (`Quadrature`)
**Module:** `src/numanalysislib/calculus/integrator.py`
- **Goal:** Compute $\int_a^b p(x) dx$ for any `PolynomialBasis` object. If the basis allows (e.g., Monomials), compute exact integral.
- **Implementation:** Provide **Gauss-Legendre** quadrature rules.

### Task 12: Differentiation Engine (`Differentiator`)
**Module:** `src/numanalysislib/calculus/differentiator.py`
- **Goal:** Compute $p'(x)$. Returns a new `PolynomialBasis object representing the derivative (if closed form exists) OR simply evaluates the derivative at points.
- **Challenge:** Must handle the affine scaling factor correctly for different domains.

### Task 13: The Plotting Suite (`Plotter`)
**Module:** `src/numanalysislib/plotting.py`
- **Goal:** Provide plotting functionalities for any `PolynomialBasis` object, such `plot_basis()`, `plot_approximation()`, etc., using Matplotlib. Consider error metrics and convergence rates as well.

### Task 14: L2 Projector (`L2Projector`)
**Module:** `src/numanalysislib/approximation/l2_project.py`
- **Goal:** Implement "best fit" by solving the system $Mc = b$ (Mass Matrix). 
  - $M_{ij} = \int \phi_i(x) \phi_j(x) dx$ (Mass Matrix).
  - $b_i = \int f(x) \phi_i(x) dx$ (Load Vector).
- **Collaboration:** Requires the Integration module (Task 11).
