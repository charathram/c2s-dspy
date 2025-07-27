# C2S-DSPy: Code-to-Summary with DSPy

A Python project that leverages DSPy (Declarative Self-improving Python) to generate intelligent summaries of code files using Azure OpenAI services.

## Overview

C2S-DSPy is designed to automatically analyze code files and generate meaningful summaries using advanced language models. The project uses DSPy's chain-of-thought reasoning to provide structured, high-quality code summaries with confidence scoring and metadata tracking.

## Features

- **Intelligent Code Summarization**: Generates human-readable summaries of code files
- **Multiple Language Support**: Works with various programming languages (Python, JavaScript, C++, COBOL, etc.)
- **Structured Output**: Uses Pydantic models for type-safe, validated data structures
- **Confidence Scoring**: Provides confidence levels for generated summaries
- **Azure OpenAI Integration**: Leverages Azure's GPT models through DSPy
- **Metadata Tracking**: Automatically tracks creation timestamps and file information
- **Neo4j Graph Database**: Store and query code analysis results as graph data
- **Comprehensive Logging**: Structured logging with performance monitoring and debug capabilities

## Installation

### Prerequisites

- **UV package manager** (recommended) - An extremely fast Python package manager
- Azure OpenAI service access
- Python 3.12+ (automatically managed by UV)

### Setup

1. **Install UV** (if not already installed):
```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using Homebrew (macOS)
brew install uv
```

2. Clone the repository:
```bash
git clone <repository-url>
cd c2s-dspy
```

3. Install dependencies using UV:
```bash
uv sync
```

4. Set up environment variables by creating a `.env` file:

**Option 1: Use the provided template (Recommended)**
```bash
cp env-template.txt .env
# Then edit .env with your actual credentials
```

**Option 2: Create .env manually**
```env
# Azure OpenAI Configuration (Required)
AZURE_API_KEY=your_azure_api_key
AZURE_API_BASE=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT=your_deployment_name
AZURE_API_VERSION=2025-04-01-preview

# Logging Configuration (Optional)
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_TO_CONSOLE=true
LOG_DIR=./logs
```

**Important**: 
- Replace `your_azure_api_key`, `your-resource`, and `your_deployment_name` with your actual Azure OpenAI credentials
- The `env-template.txt` file contains detailed explanations for each setting
- Never commit the `.env` file to version control (it's already in `.gitignore`)

**📖 For detailed UV usage instructions, see [docs/uv-usage.md](docs/uv-usage.md)**

## Usage

### Basic Code Summarization

Analyze a specific file from the sample inputs:

```bash
uv run c2s.py -f sample_inputs/COACTUPC.cbl
```

Or analyze all files in a directory:

```bash
uv run c2s.py -d sample_inputs
```

Or analyze the default sample (when neither -f nor -d is specified):

```bash
uv run c2s.py
```

**Note**: The `-f` (file) and `-d` (directory) options are mutually exclusive - you can specify one or the other, but not both.

## Project Structure

```
c2s-dspy/
├── README.md                 # This file
├── pyproject.toml           # Project configuration
├── .env                     # Environment variables (not in git)
├── models.py                # Pydantic data models
├── c2s.py                   # Main code-to-summary implementation
├── main.py                  # Basic DSPy example
├── example_usage.py         # Usage examples and demonstrations
├── utils.py                 # Utility functions for file operations
├── logging_config.py        # Centralized logging configuration
├── example_logging.py       # Logging usage examples
├── env-template.txt         # Environment configuration template
├── Makefile                 # Neo4j management commands
├── docker-compose.yml       # Neo4j container configuration
├── docs/
│   ├── neo4j-setup.md       # Neo4j setup and usage guide
│   └── uv-usage.md          # UV package manager usage guide
├── logs/                    # Log files directory (auto-created)
├── sample_inputs/           # Sample code files for testing
│   ├── ACCTFILE.jcl         # JCL job control language sample
│   ├── COACTUP.CPY          # COBOL copybook sample
│   ├── COACTUP.bms          # BMS map definition sample
│   ├── COACTUPC.cbl         # COBOL program sample
│   ├── COADM02Y.cpy         # COBOL copybook sample
│   └── sample_code.cbl      # Basic COBOL code sample
└── .gitignore              # Git ignore rules
```

## Core Components

### CodeSummary Model (`models.py`)

A Pydantic model that structures the output with the following fields:

- `filename`: Name or path of the code file (required)
- `summary`: AI-generated summary of the code (required)
- `language`: Programming language of the file (optional)
- `created_at`: Timestamp when summary was created (auto-generated)
- `confidence_score`: Confidence level from 0.0 to 1.0 (optional)

### Code Summarization (`c2s.py`)

Main implementation that:
- Loads environment configuration
- Configures DSPy with Azure OpenAI
- Uses Chain-of-Thought reasoning for code analysis
- Outputs structured CodeSummary objects

## Configuration

The project uses environment variables for configuration:

### Azure OpenAI Configuration

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `AZURE_API_KEY` | Your Azure OpenAI API key | `abc123...` | Yes |
| `AZURE_API_BASE` | Azure OpenAI endpoint URL | `https://your-resource.openai.azure.com/` | Yes |
| `AZURE_DEPLOYMENT` | Deployment name in Azure | `gpt-4o` | Yes |
| `AZURE_API_VERSION` | API version to use | `2024-02-01` | Yes |

### Logging Configuration

| Variable | Description | Options | Default |
|----------|-------------|---------|---------|
| `LOG_LEVEL` | Logging verbosity level | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `INFO` |
| `LOG_TO_FILE` | Enable file logging | `true`, `false` | `true` |
| `LOG_TO_CONSOLE` | Enable console logging | `true`, `false` | `true` |
| `LOG_DIR` | Directory for log files | Any valid path | `./logs` |

## Neo4j Graph Database

This project includes a complete Neo4j setup for storing and querying code analysis results as graph data. Neo4j is perfect for analyzing code relationships, dependencies, and data model connections.

### Quick Start with Neo4j

```bash
# Start Neo4j database
make start

# Check status
make status

# Open web interface
make web
```

**📖 For complete Neo4j setup, configuration, and usage instructions, see [docs/neo4j-setup.md](docs/neo4j-setup.md)**

### Neo4j Management Commands

| Command | Description |
|---------|-------------|
| `make start` | Start Neo4j database |
| `make stop` | Stop Neo4j database |
| `make status` | Show Neo4j status |
| `make shell` | Open Cypher shell |
| `make backup` | Create database backup |
| `make web` | Open web interface |
| `make help` | Show all commands |

### Connection Details

- **Web Interface**: http://localhost:7474
- **Bolt Connection**: bolt://localhost:7687
- **Username**: `neo4j`
- **Password**: `password123`

## Logging System

C2S-DSPy includes a comprehensive logging system that provides structured logging, performance monitoring, and debugging capabilities.

### Logging Features

- **Colored Console Output**: Different colors for different log levels
- **File Logging**: Automatic log file rotation with configurable size limits
- **Performance Monitoring**: Built-in timing for operations
- **Multiple Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Structured Output**: Detailed context for debugging
- **Environment Configuration**: Control via environment variables

### Quick Start with Logging

```bash
# Run with default settings from .env file
uv run c2s.py

# Override LOG_LEVEL for one-time debug session
LOG_LEVEL=DEBUG uv run c2s.py

# Override multiple logging settings
LOG_LEVEL=DEBUG LOG_TO_FILE=false uv run c2s.py

# Run logging examples
uv run example_logging.py

# Test debug logging behavior
uv run test_debug_logging.py
```

### Environment Variables for Logging

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |
| `LOG_TO_FILE` | Enable file logging (true/false) | `true` |
| `LOG_TO_CONSOLE` | Enable console logging (true/false) | `true` |
| `LOG_DIR` | Directory for log files | `./logs` |

### Logging in Code

```python
from logging_config import get_default_logger, PerformanceLogger

# Get logger
logger = get_default_logger()

# Basic logging
logger.info("Processing started")
logger.debug("Detailed debug information")
logger.error("An error occurred")

# Performance monitoring
with PerformanceLogger() as perf:
    perf.start("operation_name")
    # Your code here
    # Automatically logs duration on exit
```

### Log Files

- **Location**: `./logs/` directory
- **Format**: `c2s-dspy.log` (with automatic rotation)
- **Retention**: 5 backup files kept automatically
- **Size Limit**: 10MB per file before rotation

### Debug Messages Not Appearing?

If debug messages aren't showing up (like line 88 in c2s.py), it's because:

1. **Default Level**: The logger defaults to INFO level (20)
2. **DEBUG Level**: Debug messages have level 10 (lower than INFO)
3. **Filtering**: Messages below the logger's level are filtered out

**Solutions**:

1. **Set LOG_LEVEL in .env file (Recommended)**:
```env
LOG_LEVEL=DEBUG
```

2. **Override for one-time use**:
```bash
LOG_LEVEL=DEBUG uv run c2s.py
```

3. **Set permanently in shell**:
```bash
export LOG_LEVEL=DEBUG  # Linux/macOS
set LOG_LEVEL=DEBUG     # Windows
```

**Test the logging behavior**:
```bash
uv run test_debug_logging.py
```

### File Utilities

The project includes utilities for file operations with advanced filtering:

```python
from utils import get_all_files, get_all_files_generator, get_files_by_extension

# Get all files in a directory
files = get_all_files("sample_inputs")

# Ignore specific file extensions
files = get_all_files("sample_inputs", ignore_extensions=['.log', '.tmp'])

# Generator version for memory efficiency
for file_path in get_all_files_generator("sample_inputs", ignore_extensions=['.bak']):
    process_file(file_path)

# Get files by extension with ignore list
py_files = get_files_by_extension(".", ".py", ignore_extensions=['.pyc', '.pyo'])
```

**Features**:
- **Extension normalization**: Handles `.ext`, `ext`, case variations
- **Recursive scanning**: Searches all subdirectories
- **Memory efficient**: Generator version available
- **Flexible filtering**: Multiple extensions supported

## Examples

### Sample Input Files

The project includes various sample files in the `sample_inputs/` directory for testing different code types:

- **`COACTUPC.cbl`** - Complete COBOL program with data structures
- **`COACTUP.CPY`** - COBOL copybook with data definitions  
- **`COACTUP.bms`** - BMS map definition for screen layouts
- **`ACCTFILE.jcl`** - JCL job control language script
- **`COADM02Y.cpy`** - Additional COBOL copybook sample
- **`sample_code.cbl`** - Basic COBOL code example

### Analyzing Sample Files

```bash
# Analyze a specific COBOL program
uv run c2s.py -f sample_inputs/COACTUPC.cbl

# Analyze a specific copybook
uv run c2s.py -f sample_inputs/COACTUP.CPY

# Analyze a specific BMS map
uv run c2s.py -f sample_inputs/COACTUP.bms

# Analyze all files in the sample directory
uv run c2s.py -d sample_inputs

# Note: Cannot use both -f and -d together
# This will show an error: uv run c2s.py -f file.py -d directory
```

The system demonstrates its ability to handle legacy mainframe code and extract meaningful summaries from various file types.

## Development

### Running Examples

1. **Basic DSPy Example**:
```bash
uv run main.py
```

2. **Code Summarization Example**:
```bash
uv run c2s.py
```

3. **Model Usage Examples**:
```bash
uv run example_usage.py
```

### Testing Logging

Run the logging examples to see all features:

```bash
# Basic logging example
uv run example_logging.py

# Override log level temporarily
LOG_LEVEL=DEBUG uv run example_logging.py
LOG_LEVEL=WARNING uv run example_logging.py

# Override logging settings (console only)
LOG_TO_FILE=false uv run example_logging.py

# Multiple overrides
LOG_LEVEL=DEBUG LOG_TO_CONSOLE=false uv run example_logging.py

# Test debug logging behavior
uv run test_debug_logging.py

# Test ignore_extensions functionality
uv run test_ignore_extensions.py
```

## Dependencies

- **DSPy** (≥2.6.27): Declarative self-improving Python
- **OpenAI** (≥1.85.0): Azure OpenAI integration
- **Pydantic** (≥2.0.0): Data validation and settings management
- **Python-dotenv** (≥1.1.0): Environment variable loading

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Environment Variables Not Found**: Ensure your `.env` file is in the project root and contains all required variables.

2. **Azure OpenAI Authentication**: Verify your API key and endpoint URL are correct.

3. **Model Validation Errors**: Check that your CodeSummary fields meet the validation requirements (non-empty strings, confidence scores between 0.0-1.0).

### Getting Help

- Check the example files for usage patterns
- Review the DSPy documentation for advanced features
- Ensure your Azure OpenAI deployment is active and accessible

## Acknowledgments

- Built with [DSPy](https://dspy.ai) for intelligent prompt engineering
- Uses [Pydantic](https://pydantic.dev/) for robust data validation
- Powered by Azure OpenAI services
