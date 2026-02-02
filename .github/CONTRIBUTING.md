# Contribution Guidelines

To maintain a high-quality scientific library, all contributors must follow these coding standards. Our goal is to write code that is "self-documenting" and mathematically robust.

---

## 1. Python Style Guide (PEP 8)
We follow the standard [PEP 8](https://peps.python.org/pep-0008/) style guide. Key rules:
- **Indentations:** Use 4 spaces per indentation level.
- **Line Length:** Limit all lines to a maximum of 79 characters.
- **Naming Conventions:**
    - **Classes:** `PascalCase` (e.g., `LagrangePolynomial`)
    - **Functions & Variables:** `snake_case` (e.g., `evaluate_basis`)
    - **Constants:** `UPPER_CASE_WITH_UNDERSCORES` (e.g., `MAX_ITERATIONS`)

## 2. Type Hinting
Modern Python uses type hints to make code easier to debug and read. Every function you write must include hints.

**Example:**
```python
def interpolate(self, x_nodes: np.ndarray, y_nodes: np.ndarray) -> np.ndarray:
    """Computes coefficients from nodes."""
    # Your code here
    return coefficients
```

## 3. Vectorization over Loops
Performance is critical in numerical analysis. Avoid for loops when performing mathematical operations on arrays. Use numpy functions instead.

**Bad**:
```python
for i in range(len(x)):
    y[i] = x[i] ** 2
```

**Good**:
```python
y = np.square(x)
```

## 4. Documentation (Docstrings)
We use the NumPy style for docstrings. Each class and method should describe its mathematical purpose and the shape of the input arrays.
```python
def evaluate(self, coefficients: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    Evaluates the polynomial at given points.

    Parameters
    ----------
    coefficients : np.ndarray
        Array of shape (n_dofs,) containing the basis coefficients.
    x : np.ndarray
        Points at which to evaluate the polynomial.

    Returns
    -------
    np.ndarray
        The evaluated values, same shape as x.
    """
```

## 5. Mathematical Stability
When implementing your algorithms, consider numerical stability. If an algorithm is known to be unstable under certain conditions, add a warning using the `warnings` module.

## 6. Testing Requirements
No Pull Request will be merged without corresponding tests in the tests/ directory.
- Test against known analytical results (e.g., a degree 2 polynomial should perfectly reconstruct $x^2$).
- Use `np.testing.assert_allclose(actual, desired, atol=1e-12)` to handle floating-point precision issues.

## 7. The Workflow in a Nutshell
- Fork and Clone.
- Branch from `main`.
- Write Code + Write Tests.
- Run `pytest` locally.
- Push and open a Pull Request.
- Respond to peer review comments.