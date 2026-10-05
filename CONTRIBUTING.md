# Contributing to Ham Clock

Thanks for your interest in contributing to Ham Clock! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear, descriptive title**
- **Describe the exact steps which reproduce the problem** in as many details as possible
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs** if possible
- **Include your environment details**: OS, Python version, Kivy version, etc.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **A clear, descriptive title**
- **A detailed description of the suggested enhancement** with as many specific examples as possible
- **Why this enhancement would be useful** to most Ham Clock users
- **Links to any related discussions or issues**

### Pull Requests

- Fill in the required template
- Follow the Python and Kivy style guidelines
- Include appropriate test cases (if applicable)
- Update documentation as needed
- Make sure all existing tests pass (when implemented)

## Development Setup

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/ham_clock.git
cd ham_clock
```

2. **Create a development branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Create virtual environment**
```bash
python3 -m venv ham_clock_env
source ham_clock_env/bin/activate
pip install -r requirements.txt
```

4. **Make your changes**
```bash
# Edit files
python3 ham_clock_main.py  # Test your changes
```

5. **Commit with clear messages**
```bash
git commit -m "Add feature: clear description of what was added"
```

6. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

7. **Submit a Pull Request**

## Style Guidelines

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use descriptive variable and function names
- Add docstrings to classes and functions
- Keep lines under 100 characters
- Use type hints where appropriate

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add real-time solar flux data from NOAA

- Fetch solar flux values from NOAA API
- Update Propagation screen display
- Add fallback values if API unavailable

Fixes #123
```

### Documentation

- Keep README.md up to date with any changes
- Update CHANGELOG.md for notable changes
- Add inline comments for complex logic
- Document any new data sources or APIs

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project maintainer. All complaints will be reviewed and investigated.

## Questions?

Feel free to open an issue or start a discussion if you have any questions about contributing!

---

**Thank you for contributing to Ham Clock!** 🎙️
