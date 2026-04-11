# Contributing to Pygets

Thank you for your interest in contributing to Pygets! This document provides guidelines and information to help you get started.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Getting Started

Pygets is a Python library for creating GUI widgets. Contributions are welcome in the form of bug fixes, new features, documentation improvements, or tests.

Before contributing, please:

1. Fork the repository on GitHub.
2. Clone your fork locally.
3. Create a new branch for your changes.

## Development Setup

To set up a development environment:

1. Ensure you have Python 3.10+ installed.
2. Install the project in editable mode with development tools:
   ```bash
   pip install -e .[dev]
   ```
3. Run the test suite before opening a pull request.

The project structure is as follows:

- `pygets/`: Main source code
  - `core/`: Core functionality (theme.py, widgets.py)
  - `utils/`: Utilities (colors.py, validators.py)
  - `widgets/`: Widget implementations (button.py, checkbox.py, etc.)
- `tests/`: Unit tests for each widget (test_button.py, test_checkbox.py, etc.)

## Coding Standards

- Follow PEP 8 style guidelines.
- Use descriptive variable and function names.
- Add docstrings to all public functions and classes.
- Keep lines under 80 characters where possible.

## Testing

Pygets uses pytest for testing. To run tests:

```bash
pytest tests
```

Ensure all tests pass before submitting changes. Add tests for new features or bug fixes.

## Submitting Changes

1. Commit your changes with clear, descriptive messages.
2. Push to your fork.
3. Create a pull request on GitHub.
4. Describe the changes and reference any related issues.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. Provide as much detail as possible, including steps to reproduce.

We appreciate your contributions!
