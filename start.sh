#!/bin/bash

# Activate virtual environment
source env/bin/activate

# Install or update dependencies
pip install -r requirements.txt

# Start the FastAPI application
python -m uvicorn main:app --host 0.0.0.0 --port 8000 