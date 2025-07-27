# UV Usage Guide for C2S-DSPy

This guide explains how to use UV (an extremely fast Python package manager) with the C2S-DSPy project.

## Table of Contents

- [What is UV?](#what-is-uv)
- [Installation](#installation)
- [Basic UV Commands](#basic-uv-commands)
- [Project Usage](#project-usage)
- [Environment Management](#environment-management)
- [Running Scripts](#running-scripts)
- [Dependency Management](#dependency-management)
- [Troubleshooting](#troubleshooting)

## What is UV?

UV is an extremely fast Python package manager and project manager, written in Rust. It's designed as a drop-in replacement for pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more.

### Key Benefits:
- **Speed**: 10-100x faster than pip
- **All-in-one**: Replaces multiple tools
- **Zero configuration**: Works out of the box
- **Cross-platform**: Works on macOS, Linux, and Windows

## Installation

### Install UV

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip (if you have Python already)
pip install uv

# Using Homebrew (macOS)
brew install uv
```

### Verify Installation

```bash
uv --version
```

## Basic UV Commands

### Project Management

```bash
# Create a new project
uv init my-project

# Initialize in existing directory
uv init

# Install dependencies from pyproject.toml
uv sync

# Add a dependency
uv add requests

# Add a development dependency
uv add --dev pytest

# Remove a dependency
uv remove requests
```

### Python Version Management

```bash
# List available Python versions
uv python list

# Install a specific Python version
uv python install 3.12

# Use a specific Python version for project
uv python pin 3.12
```

## Project Usage

### Setting Up C2S-DSPy

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd c2s-dspy
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

### Running C2S-DSPy Scripts

All Python scripts in this project should be run using `uv run`:

```bash
# Main code analysis
uv run c2s.py

# Analyze specific file
uv run c2s.py -f sample_inputs/COACTUPC.cbl

# Basic DSPy example
uv run main.py

# Logging examples
uv run example_logging.py

# With environment variables
LOG_LEVEL=DEBUG uv run c2s.py

# Multiple environment variables
LOG_LEVEL=DEBUG LOG_TO_FILE=false uv run example_logging.py
```

## Environment Management

### Virtual Environment

UV automatically manages virtual environments for you:

```bash
# UV automatically creates and manages .venv/
uv sync

# Activate the environment manually (usually not needed)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Run commands in the environment (preferred method)
uv run python --version
uv run pip list
```

### Environment Information

```bash
# Show environment information
uv info

# Show project information
uv tree

# Show installed packages
uv pip list
```

## Running Scripts

### Standard Usage

```bash
# Run any Python script
uv run script_name.py

# Run with arguments
uv run c2s.py --file sample_inputs/example.cbl

# Run with environment variables
ENV_VAR=value uv run script.py
```

### Interactive Python

```bash
# Start Python REPL
uv run python

# Start IPython (if installed)
uv run ipython

# Run Python with modules
uv run python -m module_name
```

### Script with Different Python Versions

```bash
# Run with specific Python version
uv run --python 3.12 script.py

# Run with system Python
uv run --python system script.py
```

## Dependency Management

### Adding Dependencies

```bash
# Add runtime dependency
uv add dspy-ai

# Add with version constraint
uv add "dspy-ai>=2.6.27"

# Add development dependency
uv add --dev pytest

# Add optional dependency
uv add --optional testing pytest
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific dependency
uv add "dspy-ai@latest"

# Update development dependencies
uv sync --upgrade --dev
```

### Viewing Dependencies

```bash
# Show dependency tree
uv tree

# Show outdated packages
uv pip list --outdated

# Export requirements
uv pip freeze > requirements.txt
```

## Troubleshooting

### Common Issues

#### 1. UV Command Not Found

```bash
# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc

# Or restart your terminal
```

#### 2. Python Version Issues

```bash
# Check available Python versions
uv python list

# Install required Python version
uv python install 3.12

# Set project Python version
uv python pin 3.12
```

#### 3. Dependency Conflicts

```bash
# Force reinstall dependencies
uv sync --reinstall

# Clear cache
uv cache clean

# Fresh install
rm -rf .venv
uv sync
```

#### 4. Environment Variables

```bash
# Check if environment variables are loaded
uv run python -c "import os; print(os.getenv('AZURE_API_KEY'))"

# Load .env file explicitly (if needed)
uv run --env-file .env python script.py
```

### Performance Tips

1. **Use UV for everything**: Replace `pip`, `python`, and other tools with `uv run`
2. **Keep dependencies minimal**: Only add what you need
3. **Use version constraints**: Pin important dependencies
4. **Regular updates**: Keep UV and dependencies updated

### Debugging

```bash
# Verbose output
uv -v sync

# Very verbose output
uv -vv run script.py

# Show UV configuration
uv info

# Check project structure
uv tree
```

### Migration from Pip/Poetry

If migrating from pip or poetry:

```bash
# From requirements.txt
uv add -r requirements.txt

# From poetry
# UV can read pyproject.toml directly
uv sync
```

## Best Practices for C2S-DSPy

1. **Always use `uv run`** instead of direct Python commands
2. **Set up environment variables** in `.env` file
3. **Use specific Python version** for consistency:
   ```bash
   uv python pin 3.12
   ```
4. **Regular dependency updates**:
   ```bash
   uv sync --upgrade
   ```
5. **Clean development environment**:
   ```bash
   uv sync --dev
   ```

## Examples Specific to C2S-DSPy

### Development Workflow

```bash
# Set up project
git clone <repository>
cd c2s-dspy
uv sync

# Run tests
uv run pytest  # (if tests are added)

# Code analysis
uv run c2s.py -f sample_inputs/COACTUPC.cbl

# Debug with logging
LOG_LEVEL=DEBUG uv run c2s.py

# Performance testing
uv run example_logging.py
```

### Neo4j Integration

```bash
# Start Neo4j
make start

# Run analysis and store in Neo4j
uv run c2s.py -f sample_inputs/COACTUPC.cbl

# Check Neo4j status
make status
```

### Batch Processing

```bash
# Process multiple files
for file in sample_inputs/*.cbl; do
    echo "Processing $file"
    uv run c2s.py -f "$file"
done
```

This guide should help you effectively use UV with the C2S-DSPy project for faster, more reliable Python package and environment management.