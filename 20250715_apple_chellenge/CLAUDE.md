# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python package that solves an algorithmic problem: counting pairs of integers in an array where the difference between two numbers equals a given value `k`. The solution uses an efficient O(n) hash map approach with proper modular arithmetic.

## Development Commands

### Environment Setup
```bash
uv sync                    # Install dependencies and set up virtual environment
```

### Testing
```bash
uv run python -m unittest discover tests/ -v    # Run all tests with verbose output
uv run python -m unittest tests.test_comprehensive.TestSolution.test_example_case  # Run single test
uv run python tests/debug_test.py               # Run debug script for manual verification
```

### Package Management
```bash
uv add <package_name>      # Add new dependency
uv run abk-aapl            # Run the CLI entry point
```

### Code Quality
```bash
uv run ruff check          # Lint code
uv run ruff format         # Format code
uv run coverage run -m unittest discover tests/  # Run tests with coverage
uv run coverage report     # Show coverage report
```

## Architecture

### Core Algorithm
- **Problem**: Count pairs `(i,j)` where `i ≠ j` and `a[j] - a[i] = k`
- **Approach**: Hash map frequency counting + target lookup
- **Time Complexity**: O(n), **Space Complexity**: O(n)
- **Key Detail**: Results are returned modulo `10^9 + 7`

### Package Structure
```
src/abk_aapl/
├── __init__.py           # Package entry point with example usage
├── solution.py           # Main optimized solution
└── simple_solution.py    # Alternative implementation
```

### Test Organization
- `test_comprehensive.py` - Main unittest suite with 17 test cases
- `test_edge_cases.py` - Edge cases (empty arrays, None inputs)  
- `test_performance.py` - Performance tests with large datasets
- `debug_test.py` - Manual verification and debugging

### Algorithm Implementations
Both `solution.py` and `simple_solution.py` implement the same logic but differ in modulo application:
- `solution.py`: Applies modulo during accumulation
- `simple_solution.py`: Applies modulo only at the end

The algorithm counts element frequencies, then for each number `num`, checks if `num + k` exists and multiplies their frequencies to count valid pairs.

## Requirements
- Python 3.13+
- Uses `uv` for package management
- All tests must pass before code changes are considered complete