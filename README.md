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

## Examples

### Summarizing a Python Script

The project includes an example that summarizes a COBOL program, demonstrating the system's ability to handle legacy code:

```python
# Example COBOL program summarization
code = """
****************************************************************
*  This program demonstrates the following Language            *
*  Environment callable services : CEEMOUT, CEELOCT, CEEDATE  *
****************************************************************
Identification Division.
Program-id.    AWIXMP.
...
"""

response = dspy.ChainOfThought("code -> summary: CodeSummary")
result = response(code=code)
```

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
