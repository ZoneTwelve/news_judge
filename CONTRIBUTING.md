# Contributing to FFHC News Inferencer

Thank you for your interest in contributing to the FFHC News Inferencer project! This document provides guidelines for contributing.

## Getting Started

1. **Fork the repository** and clone it locally
2. **Set up your development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```
3. **Copy `.env.example` to `.env`** and configure your OpenAI API key

## Development Guidelines

### Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Write docstrings for all functions and classes (Google style)
- Add type hints to function signatures
- Keep functions focused and single-purpose

### Code Formatting

We use automated tools for code quality:

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with ruff
ruff check .

# Type checking with mypy
mypy .
```

### Testing

- Write tests for new features and bug fixes
- Ensure all tests pass before submitting:
  ```bash
  pytest
  ```
- Maintain or improve code coverage

### Commit Messages

Write clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Include detailed description if needed

Example:
```
Fix typo in README documentation

Changed "exmaple" to "example" throughout the README
and fixed other minor spelling issues.
```

## Submitting Changes

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test your changes** thoroughly

4. **Commit your changes** with clear messages

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues (if any)
   - Screenshots for UI changes (if applicable)

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

## Questions?

Feel free to open an issue for questions or discussions about the project!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
