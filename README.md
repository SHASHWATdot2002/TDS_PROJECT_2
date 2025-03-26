# FastAPI Language Model API

A FastAPI application that provides an API interface to interact with language models through HuggingFace's API.

## Features

- Integration with HuggingFace's API
- Default model: Mistral (optimized for better response quality)
- Simple REST API endpoints for text generation
- Improved prompt formatting for accurate responses

## Prerequisites

- Python 3.8+
- HuggingFace API key

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
export HUGGINGFACE_API_KEY=your_api_key_here
```

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

