# Collaborative Numerical Analysis Library for MATH 516 - SP26

This repository is designed for the graduate course in Numerical Analysis at Emory (MATH 516). Instead of simply solving exercises in isolation, you will work together to build a Python package from the ground up.

Our goal is to implement a robust library for function approximation, interpolation, and calculus, following modern software engineering standards.


## 🏁 The Core Idea
The mathematical backbone of this project is the concept of a Vector Space. In numerical analysis, we often approximate complex functions by projecting them onto a finite-dimensional subspace spanned by a set of basis functions $\{\phi_0, \phi_1, \dots, \phi_n\}$.

Whether we are using Lagrange polynomials, Chebyshev nodes, or Splines, the underlying logic remains the same:
$$p(x) = \sum_{i=0}^{n} c_i \phi_i(x)$$

By defining a shared Abstract Base Class, we ensure that any utility developed for one basis will automatically work for every other basis implemented by your colleagues.

## 📦 What this Repository Contains
This package, `numanalysislib`, is organized into three main pillars:

1. **The Basis Engines**: A collection of modules implementing various polynomial families. You will be responsible for defining how these functions are evaluated and how they "fit" a set of data points (Interpolation).

2. **The Calculus Operators**: High-level utilities that perform numerical integration and differentiation. These modules are "basis-agnostic" as they treat the polynomials as black boxes, allowing for powerful code reuse.

3. **The Validation Suite**: A comprehensive set of unit tests. Reliability is the hallmark of scientific computing; therefore, no feature is considered "done" until it passes a rigorous battery of automated tests.


## 🛠 Your Role as a Contributor
As a student in this course, you will act as a Library Maintainer. You will be assigned a specific module to implement, but your responsibilities go beyond just writing code:

1. **Collaborate**: You must ensure your module plays nicely with others.
2. **Test**: You will write unit tests to prove your implementation's accuracy.
3. **Review**: You will participate in the Peer Review process via GitHub Pull Requests, helping your classmates improve their code.

By the end of the semester, we will use our collective work to solve a complex problem such as reconstructing and analyzing the dynamics of a parametric system, demonstrating the power of modular, collaborative design.

## 🍴 How to Contribute: The Forking Workflow
To maintain a clean codebase, we follow the **Forking Workflow**. This allows you to experiment freely in your own copy of the project before proposing your changes to the main library.

1. Fork the Official Repository. Click the Fork button at the top-right of this GitHub page. This creates a personal copy of the repository under your GitHub account.

2. Clone Your Fork. Download your copy of the code to your local machine:

```bash
git clone https://github.com/YOUR-USERNAME/math-516-numerical-analysis-II-SP26.git numerical-analysis-course
cd numerical-analysis-course
```

3. Connect to the Upstream Repository. To keep your fork updated with the latest changes, add the original repository as a remote named upstream:

```bash
git remote add upstream https://github.com/mtezzele/math-516-numerical-analysis-II-SP26.git
```

4. Create a Feature Branch. Never work directly on the main branch. Create a new branch for your specific assignment (e.g., `lagrange-basis`):

```bash
git checkout -b your-topic-name
```

5. Commit and Push. Once you have implemented your class and passed your tests, push your code to your fork on GitHub:

```bash
git add filename1 filename2
git commit -m "DESCRIBE YOUR EDITS"
git push origin your-topic-name
```

6. Open a Pull Request (PR). Go to the original repository on GitHub. You should see a prompt to "Compare & pull request". 

* Provide a clear description of what you implemented.

* Ensure all GitHub Actions (the automated tests) turn green.

* Your colleagues and the instructor will review your code. Once approved, it will be merged into the main library!



## How to install
In order to use and develop this library follow these instructions.

1. Start by creating a Virtual Environment that will keep your project isolated from your system Python.

```bash
# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

If you are already confortable with conda, go ahead and use a conda env.

2. Install the package in **editable** mode (`-e`). This means changes you make to the code are immediately reflected without reinstalling.

```bash
pip install -e '.[test]'
```

Note the `[test]` part that tells pip to also install the testing tools listed in `pyproject.toml` like `pytest`.

3. To check if your code works, run the tests with:

```bash
pytest tests/
```

