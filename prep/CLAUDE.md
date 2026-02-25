# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses `just` as the task runner with `uv` for Python dependency management:

- `just install` - Install all dependencies using uv
- `just demo` - Run the demo interview code
- `just test` - Run unit tests
- `just coverage` - Run tests with coverage reporting (generates HTML report)
- `just clean` - Clean up coverage artifacts

## Project Architecture

This is a Python project demonstrating multiple inheritance and method resolution order (MRO). The codebase structure:

- `src/demo/interview.py` - Main module with classes A, B, C, D demonstrating diamond inheritance pattern
- `tests/demo/test_interview.py` - Comprehensive tests for all classes and MRO behavior
- Entry point: `interview` command runs `src.demo.interview:main`

## Key Technical Details

- **Python Version**: Requires Python 3.13+
- **Linting**: Uses ruff with strict configuration (line length 130, Google docstring style)
- **Testing**: pytest with coverage reporting
- **Package Structure**: Source code in `src/` directory, tests mirror structure in `tests/`
- **MRO Focus**: Class D inherits from both B and C (which both inherit from A), demonstrating Python's C3 linearization

## Code Quality Standards

- All code must pass ruff linting with the configured ruleset
- Test coverage tracking is configured to include all source files
- Docstrings follow Google style convention