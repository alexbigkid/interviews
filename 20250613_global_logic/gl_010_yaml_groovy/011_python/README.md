# GL 011 - Python Implementation

Python implementation with dual CI/CD options: GitHub Actions and Jenkins.

## Features

- **Hello Global Logic**: Simple greeting function
- **Fizz Buzz**: Classic programming challenge implementation  
- **Metadata Processing**: Reactive programming with ReactiveX

## Development

### Prerequisites
- Python 3.13+
- uv package manager

### Installation
```bash
uv sync --group dev
```

### Running Applications
```bash
# Using project scripts
uv run hello
uv run fizz_buzz  
uv run meta_data

# Or run modules directly
uv run python -m gl_011.hello_global_logic
uv run python -m gl_011.fizz_buzz
uv run python -m gl_011.meta_data
```

### Testing
```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov --cov-report=html
```

## CI/CD Options

This project demonstrates the same pipeline implemented in two different CI/CD systems:

### 1. GitHub Actions (YAML)
- **File**: `.github/workflows/gl_011_python.yml`
- **Triggers**: Push/PR to main branch
- **Features**: Matrix testing, Ruff linting, pytest with coverage

### 2. Jenkins (Groovy)
- **File**: `Jenkinsfile`
- **Triggers**: GitHub webhooks, manual builds
- **Features**: Same functionality as GitHub Actions but in Jenkins

Both pipelines provide identical functionality:
-  Ruff linting and formatting
-  Matrix testing (Python 3.13, Ubuntu/macOS)  
-  Coverage reporting
-  Codecov integration
-  Artifact archival

This allows you to choose your preferred CI/CD platform while maintaining the same build process.