# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Setup

This is a Python package project (`gl-011`) managed with `uv` (modern Python package manager). The project uses:
- Python 3.13+ requirement
- `uv` for dependency management and virtual environment
- Package structure under `src/gl_011/`

## Development Environment

The project uses `direnv` with `.envrc` for environment setup:
- Automatically syncs dependencies with `uv sync`
- Activates virtual environment on directory entry
- Sets `UV_PREVIEW=1` for uv preview features

## Common Commands

**Environment Setup:**
```bash
# Initial setup (handled by direnv)
uv sync
source .venv/bin/activate
```

**Run Tests:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_fizz_buzz.py

# Run with verbose output
pytest -v
```

**Run the application:**
```bash
# Via installed scripts
hello
fizz_buzz

# Direct module execution
python -m gl_011.hello_global_logic
python -m gl_011.fizz_buzz
```

**Package management:**
```bash
# Add dependencies
uv add <package>

# Remove dependencies  
uv remove <package>

# Update lock file
uv lock
```

## Project Structure

- `src/gl_011/` - Main package directory containing modules
  - `hello_global_logic.py` - Simple hello function
  - `fizz_buzz.py` - FizzBuzz implementation with main runner
- `tests/` - Test directory with pytest tests
- `pyproject.toml` - Project configuration with script entry points
- `uv.lock` - Locked dependency versions
- `.envrc` - Environment setup for direnv

## Package Scripts

The project defines entry point scripts in `pyproject.toml`:
- `hello` → `gl_011.hello_global_logic:hello`
- `fizz_buzz` → `gl_011.fizz_buzz:main`