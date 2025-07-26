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

## Installation

### Prerequisites

- Python 3.12 or higher
- Azure OpenAI service access
- UV package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd c2s-dspy
```

2. Install dependencies using UV:
```bash
uv sync
```

3. Set up environment variables by creating a `.env` file:
```env
AZURE_API_KEY=your_azure_api_key
AZURE_API_BASE=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT=your_deployment_name
AZURE_API_VERSION=2025-04-01-preview
```

## Usage

### Basic Code Summarization

Analyze a specific file from the sample inputs:

```bash
python3 c2s.py -f sample_inputs/COACTUPC.cbl
```

Or analyze the default sample:

```bash
python3 c2s.py
```

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
├── Makefile                 # Neo4j management commands
├── docker-compose.yml       # Neo4j container configuration
├── docs/
│   └── neo4j-setup.md       # Neo4j setup and usage guide
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

The project uses environment variables for Azure OpenAI configuration:

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_API_KEY` | Your Azure OpenAI API key | `abc123...` |
| `AZURE_API_BASE` | Azure OpenAI endpoint URL | `https://your-resource.openai.azure.com/` |
| `AZURE_DEPLOYMENT` | Deployment name in Azure | `gpt-4o` |
| `AZURE_API_VERSION` | API version to use | `2024-02-01` |

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
# Analyze a COBOL program
python3 c2s.py -f sample_inputs/COACTUPC.cbl

# Analyze a copybook
python3 c2s.py -f sample_inputs/COACTUP.CPY

# Analyze a BMS map
python3 c2s.py -f sample_inputs/COACTUP.bms
```

The system demonstrates its ability to handle legacy mainframe code and extract meaningful summaries from various file types.

## Development

### Running Examples

1. **Basic DSPy Example**:
```bash
python3 main.py
```

2. **Code Summarization Example**:
```bash
python3 c2s.py
```

3. **Model Usage Examples**:
```bash
python3 example_usage.py
```

### Dependencies

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
