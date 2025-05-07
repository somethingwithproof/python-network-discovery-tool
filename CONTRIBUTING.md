# Contributing to Network Discovery Tool

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/thomasvincent/python-network-discovery-tool/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature" is open to whoever wants to implement it.

### Write Documentation

Network Discovery Tool could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/thomasvincent/python-network-discovery-tool/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome!

## Get Started!

Ready to contribute? Here's how to set up `network-discovery` for local development.

### Using Docker (Recommended)

1. Fork the `python-network-discovery-tool` repo on GitHub.
2. Clone your fork locally:
   ```bash
   git clone git@github.com:your_name_here/python-network-discovery-tool.git
   ```
3. Use Docker Compose to set up the development environment:
   ```bash
   cd python-network-discovery-tool/
   docker-compose run dev
   ```
   This will start a development shell with all dependencies installed.

4. Create a branch for local development:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```
   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and linters:
   ```bash
   # Run tests
   docker-compose run test

   # Run linters
   docker-compose run dev bash -c "flake8 src tests && black src tests && isort src tests && mypy src tests"
   
   # Run tox
   docker-compose run dev tox
   ```

6. Commit your changes and push your branch to GitHub:
   ```bash
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

7. Submit a pull request through the GitHub website.

### Traditional Setup

1. Fork the `python-network-discovery-tool` repo on GitHub.
2. Clone your fork locally:
   ```bash
   git clone git@github.com:your_name_here/python-network-discovery-tool.git
   ```
3. Install your local copy into a virtualenv:
   ```bash
   cd python-network-discovery-tool/
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. Create a branch for local development:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```
   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and linters:
   ```bash
   # Run tests
   pytest

   # Run linters
   flake8 src tests
   black src tests
   isort src tests
   mypy src tests
   
   # Run tox
   tox
   ```

6. Commit your changes and push your branch to GitHub:
   ```bash
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
3. The pull request should work for Python 3.7, 3.8, 3.9, 3.10, 3.11, and 3.12. Check the GitHub Actions workflow and make sure that the tests pass for all supported Python versions.

## Tips

### Testing with Docker

To run a subset of tests:
```bash
docker-compose run test tests/test_scanner.py
```

To run a specific test:
```bash
docker-compose run test tests/test_scanner.py::TestNmapDeviceScanner::test_scan_device
```

### Development Workflow with Docker

1. Start the development container:
   ```bash
   docker-compose run dev
   ```

2. Make your changes inside the container.

3. Run tests to verify your changes:
   ```bash
   pytest
   ```

4. Exit the container when done:
   ```bash
   exit
   ```

## Code of Conduct

Please note that the Network Discovery Tool project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.
