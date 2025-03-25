from fastapi import FastAPI, Form, File, UploadFile, HTTPException
import requests
import zipfile
import pandas as pd
import io
import os
from typing import Optional

app = FastAPI()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434/api/generate")
MODEL_NAME = "llama2"

def check_ollama_connection():
    try:
        response = requests.get("http://127.0.0.1:11434/api/version", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def check_model_exists():
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model.get("name") == MODEL_NAME for model in models)
        return False
    except requests.exceptions.RequestException:
        return False

@app.post("/api/")
async def answer_question(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        extracted_answer = None
        
        # Handle file if provided
        if file:
            # Read the uploaded ZIP file
            zip_content = await file.read()
            with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_ref:
                # Extract CSV file from ZIP
                csv_filename = zip_ref.namelist()[0]  # Assuming one file in ZIP
                with zip_ref.open(csv_filename) as csv_file:
                    df = pd.read_csv(csv_file)
            
            # Extract answer from CSV
            if 'answer' in df.columns:
                extracted_answer = str(df['answer'].iloc[0])  # Get the first value in 'answer' column
            else:
                raise HTTPException(status_code=400, detail="Column 'answer' not found in CSV")

        # Check if Ollama is running
        if not check_ollama_connection():
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not running. Please start Ollama first using 'ollama serve' command."
            )

        # Check if model exists
        if not check_model_exists():
            raise HTTPException(
                status_code=503,
                detail=f"Model '{MODEL_NAME}' is not installed. Please install it using 'ollama pull {MODEL_NAME}' command."
            )

        # Send the question to Ollama API
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={"model": MODEL_NAME, "prompt": question},
                timeout=30  # Add timeout
            )
            response.raise_for_status()  # Raise exception for bad status codes
            response_json = response.json()
            llm_answer = response_json.get("response")
        except requests.exceptions.RequestException as e:
            if "404" in str(e):
                raise HTTPException(
                    status_code=503,
                    detail=f"Model '{MODEL_NAME}' is not installed. Please install it using 'ollama pull {MODEL_NAME}' command."
                )
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to Ollama service: {str(e)}"
            )

        return {
            "extracted_answer": extracted_answer,
            "llm_answer": llm_answer,
            "question": question
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))