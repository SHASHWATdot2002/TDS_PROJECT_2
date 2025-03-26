# FastAPI LLM Question-Answering API

A FastAPI-based REST API that provides question-answering capabilities using HuggingFace's language models. The API supports both direct questions and file-based answers through CSV uploads.

## Features

- Question answering using HuggingFace's language models
- Support for multiple models (flan-t5-base, gpt2, flan-t5-large)
- File processing for CSV files (must be zipped)
- Environment variable configuration
- Docker support
- Automatic retries for API calls

## Prerequisites

- Python 3.9 or higher
- HuggingFace API token
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and add your HuggingFace API key
5. Run the application: `uvicorn main:app --reload`

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

### Generate Text
- **POST** `/generate`
  - Request body:
    ```json
    {
      "prompt": "Your prompt here",
      "max_length": 100  // optional
    }
    ```
  - Returns generated text based on the prompt

### Health Check
- **GET** `/health`
  - Returns API health status

## Configuration

The application uses the following default settings:
- Model: Mistral
- Maximum length: 100 tokens
- Temperature: 0.7

These can be adjusted through environment variables or API parameters.

## Error Handling

The API includes robust error handling for:
- Invalid prompts
- API connection issues
- Model-specific errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

