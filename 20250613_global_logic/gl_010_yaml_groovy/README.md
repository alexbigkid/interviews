# Global Logic 010

![Python Tests](https://github.com/alexbigkid/gl_010_yaml_groovy/actions/workflows/gl_011_python.yml/badge.svg)
![TypeScript Tests](https://github.com/alexbigkid/gl_010_yaml_groovy/actions/workflows/gl_012_typescript.yml/badge.svg)
<!-- [![codecov](https://codecov.io/gh/alexbigkid/gl_010_yaml_groovy/branch/main/graph/badge.svg)](https://codecov.io/gh/alexbigkid/gl_010_yaml_groovy) -->

This repository contains multiple implementations of the same core functionality:

## Projects

### GL 011 - Python Implementation
- **Location**: `011_python/`
- **Features**: Hello Global Logic, Fizz Buzz, Reactive Metadata Processing
- **Framework**: Python with ReactiveX (RxPY)
- **Testing**: pytest with coverage
- **CI/CD**: GitHub Actions with Ruff linting

### GL 012 - TypeScript Implementation
- **Location**: `012_typescript/`
- **Features**: Hello Global Logic, Fizz Buzz, Reactive Metadata Processing
- **Framework**: TypeScript with RxJS
- **Testing**: Jest with coverage
- **CI/CD**: GitHub Actions with ESLint/Prettier

## Quick Start

### Python Project
```bash
cd 011_python
uv sync --group dev
uv run pytest --cov
```

### TypeScript Project
```bash
cd 012_typescript
npm install
npm test
npm run hello        # Run Hello Global Logic
npm run fizz-buzz    # Run Fizz Buzz
npm run meta-data    # Run Reactive Metadata Processing
```

## Common Features

Both implementations include:
- **Hello Global Logic**: Simple greeting function
- **Fizz Buzz**: Classic programming challenge
- **Metadata Processing**: Reactive programming with error handling, retries, and concurrent processing

## CI/CD

- Multi-OS testing (Ubuntu, macOS, Windows)
- Code quality checks (linting, formatting)
- Test coverage reporting
- Automated builds on push/PR to main branch
