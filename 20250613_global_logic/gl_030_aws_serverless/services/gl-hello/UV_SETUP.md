# UV Setup for Local Development

This template now supports `uv` for local development while maintaining `requirements.txt` for AWS Lambda deployment.

## Quick Start

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Sync dependencies** (recommended for local development):
   ```bash
   make sync
   ```

3. **Run tests**:
   ```bash
   make test
   ```

## Available Make Commands

### UV-based (Recommended for Local Development)
- `make sync` - Sync all dependencies using uv
- `make install` - Install dependencies using uv pip
- `make install_test` - Install test dependencies using uv pip
- `make install_all` - Install all dependencies including dev extras
- `make export_requirements` - Generate requirements.txt files for deployment

### Legacy pip commands (Fallback)
- `make install_pip` - Install using traditional pip
- `make install_test_pip` - Install test deps using traditional pip
- `make install_all_pip` - Install all deps using traditional pip

### Testing (Uses uv run)
- `make test` - Run tests using uv run
- `make test_v` - Run tests with verbose output
- `make coverage` - Run tests with coverage reporting

## Benefits of UV

- **Faster dependency resolution** and installation
- **Better dependency management** with uv.lock
- **Virtual environment management** handled automatically
- **Compatible with pip** requirements.txt for deployment

## Deployment

AWS Lambda deployment still uses `requirements.txt` files. The `make export_requirements` command generates these from your uv.lock file to ensure consistency between local development and production.