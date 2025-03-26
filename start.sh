#!/bin/bash

# Activate virtual environment if it exists
if [ -d "env" ]; then
    source env/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Start the FastAPI application using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
