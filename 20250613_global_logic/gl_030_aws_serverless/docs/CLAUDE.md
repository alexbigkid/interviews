# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Deployment Commands

### Main Deployment Flow
```bash
# Install required tools (Terraform, Serverless, AWS CLI, GNU Parallel)
./InstallTools.sh

# Deploy everything in sequence (runs 001*.sh, 002*.sh, etc.)
./deploy.sh dev us-west-2

# Individual deployment scripts (run in order)
./001_setup-env.sh dev us-west-2
./002_deploy-terraform.sh dev us-west-2
./003_deploy-services.sh dev us-west-2
```

### Required Environment Variables
```bash
export GL_ENV=dev|qa|prod
export REGION=us-east-1|us-east-2|us-west-1|us-west-2
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export TF_VAR_user=db_username
export TF_VAR_pswd=db_password
```

Use `.envrc` with `direnv` for local environment management.

## Lambda Development

### Python Development Setup (UV-based)
```bash
cd services/[lambda-name]/

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync all dependencies (recommended for local development)
make sync

# Alternative installation methods
make install        # Install dependencies using uv pip
make install_test   # Install test dependencies using uv pip
make install_all    # Install all dependencies including dev extras

# Legacy pip fallback commands (if needed)
make install_pip
make install_test_pip
make install_all_pip
```

### Testing Commands
```bash
cd services/[lambda-name]/

# Run tests (uses uv run automatically)
make test           # All tests
make test_ff        # Fail-fast mode
make test_v         # Verbose output
make test_vff       # Verbose fail-fast
make test_1 <test>  # Single test
make coverage       # Coverage report

# Generate requirements.txt for deployment from uv.lock
make export_requirements
```

### Lambda Deployment
```bash
cd services/[lambda-name]/[lambda-directory]/
serverless deploy --region $REGION --stage $GL_ENV --verbose
```

## Terraform Operations

### State Management
- Remote state stored in S3 bucket: `gl-terraform-state-do-not-delete`
- State locking via DynamoDB table: `gl-terraform-lock`
- Bootstrap required: Deploy `terraformStateBootstrap` module first

### Infrastructure Modules
```bash
cd terraform/dev/001_postgreDB/
terraform init
terraform plan -var="user=$TF_VAR_user" -var="pswd=$TF_VAR_pswd"
terraform apply
```

## Architecture Overview

### Deployment Strategy
This project uses a numbered script system (`001_*.sh`, `002_*.sh`) to ensure proper deployment order:
1. Terraform infrastructure (databases, networking)
2. Lambda functions via Serverless Framework

### Terraform Structure
- `/terraform/templates/` - Reusable modules
- `/terraform/dev|stage|prod/` - Environment-specific deployments
- `terraformStateBootstrap` - Creates S3 + DynamoDB for state management
- `postgreDB` - PostgreSQL RDS deployment

### Lambda Architecture
- **Runtime**: Python 3.11
- **Framework**: Serverless Framework v3
- **Dependency Management**: UV for local development, requirements.txt for deployment
- **Packaging**: Individual per function
- **Testing**: Make-based with coverage reporting using uv run
- **Deployment**: GNU Parallel for concurrent processing

### CI/CD Pipeline
Jenkins pipeline with environment-specific stages:
- **DEV/QA**: Auto-deploy on commits
- **PROD**: Requires `release` git tag
- **Stages**: tool installation → terraform → lambda layers → services → integration tests → cleanup
- **Notifications**: Slack integration with color-coded status

### Database Schema
PostgreSQL with tables: team, user, collaborator, project, device, model, app
- Hierarchical relationships with foreign key constraints
- Optimized queries for device listing by project

### Security Model
- S3 state encryption (AES256)
- DynamoDB locking prevents concurrent deployments
- Credential management via secure storage systems
- Environment-specific AWS profiles
