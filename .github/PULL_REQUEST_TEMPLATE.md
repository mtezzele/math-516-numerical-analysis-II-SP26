## Description
## Linked Issue
Fixes # (issue number)

## Implementation Checklist
- [ ] My class inherits from `PolynomialBasis` (if applicable).
- [ ] I have implemented all abstract methods (`evaluate_basis`, `fit`, etc.).
- [ ] I have used `numpy` vectorization to avoid inefficient Python loops.
- [ ] Documentation strings (docstrings) are provided for all public methods.

## Peer Review Checklist (To be completed by Reviewer)

### 1. Mathematical Integrity
- [ ] **Convergence:** Does the implementation maintain expected accuracy? (Checked for Runge's phenomenon or stability).
- [ ] **Edge Cases:** Does it handle single points or non-equally spaced nodes correctly?
- [ ] **Domain Mapping:** Does the class correctly map the input domain to the basis domain (e.g., [-1, 1] for Chebyshev)?

### 2. API & Style
- [ ] **Method Signatures:** Methods match the Abstract Base Class exactly.
- [ ] **Naming:** Follows `CamelCase` for classes and `snake_case` for functions/variables.
- [ ] **Clean Code:** No "magic numbers"; constants are named and explained.

### 3. Testing Quality
- [ ] **Coverage:** Unit tests cover typical usage and edge cases.
- [ ] **Precision:** Tests use `np.testing.assert_allclose` instead of `==`.
- [ ] **Validation:** There is a test proving the basis can exactly reconstruct a polynomial of its own degree.

## Screenshots / Plots