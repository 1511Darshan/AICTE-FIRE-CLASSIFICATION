# Contributing to AICTE Fire Classification

Thank you for your interest in contributing! This document outlines guidelines for reporting issues, suggesting features, and submitting pull requests.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive criticism
- Acknowledge diverse perspectives and backgrounds
- Report unacceptable behavior to the maintainers

## Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Provide a clear description** of the bug
3. **Include reproduction steps** and expected vs. actual behavior
4. **Share your environment**: Python version, OS, library versions
5. **Include error messages and traceback** if applicable

## Feature Requests

1. **Describe the feature** and its benefits
2. **Explain the use case** and why it's needed
3. **Suggest implementation approaches** if possible
4. **Check if similar features exist** elsewhere

## Pull Requests

### Before You Start

- Create a new branch: `git checkout -b feature/your-feature-name`
- Keep changes focused and modular
- Run tests locally before submitting

### Code Standards

- Follow PEP 8 (use `black` for formatting)
- Include docstrings for functions and classes
- Write clear, descriptive commit messages
- Add unit tests for new functionality

### Submitting a PR

1. **Fork the repository** and create your branch
2. **Make your changes** with clear, atomic commits
3. **Test thoroughly** (unit tests, notebook execution)
4. **Update documentation** if necessary (README, docstrings)
5. **Submit the PR** with a clear description of changes

### PR Review Process

- Maintainers will review your code within a reasonable timeframe
- Feedback may be provided; please address it promptly
- Once approved, your PR will be merged
- Your contribution will be acknowledged

## Development Setup

```bash
git clone https://github.com/1511Darshan/AICTE-FIRE-CLASSIFICATION.git
cd AICTE-FIRE-CLASSIFICATION
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
pip install black flake8 isort pytest  # Optional dev tools
```

## Running Tests

```bash
pytest tests/
```

## Code Quality Checks

```bash
black src/ tests/
flake8 src/ tests/
isort src/ tests/
```

## Questions?

Feel free to open an issue or discussion if you have questions. We're here to help!

---

**Thank you for contributing to open science and disaster response! 🔥**
