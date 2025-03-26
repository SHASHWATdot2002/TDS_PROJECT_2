from fastapi import FastAPI, Form, File, UploadFile, HTTPException
import requests
import zipfile
import pandas as pd
import io
import os
import time
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configuration
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
MAX_RETRIES = 5  # Increased maximum retries
RETRY_DELAY = 3  # Increased delay between retries

# Available models configuration
MODELS: Dict[str, str] = {
    "flan-t5-base": "https://api-inference.huggingface.co/models/google/flan-t5-base",  # Most reliable
    "gpt2": "https://api-inference.huggingface.co/models/openai-communitygpt2",  # Fast but less accurate
    "flan-t5-large": "https://api-inference.huggingface.co/models/google/flan-t5-large"  # Better but slower
}

# Default to flan-t5-base model (most reliable)
DEFAULT_MODEL = "flan-t5-large"
HUGGINGFACE_API_URL = MODELS[DEFAULT_MODEL]

def get_llm_response(question: str, model_name: Optional[str] = None) -> str:
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(status_code=503, detail="HuggingFace API key not configured")
    
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    api_url = MODELS.get(model_name, HUGGINGFACE_API_URL) if model_name else HUGGINGFACE_API_URL
    
    # Prompt format that encourages direct answers without repeating the question
    formatted_prompt = f"Give a direct answer without repeating the question: {question}"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": formatted_prompt},
                timeout=30
            )
            
            if response.status_code == 200:
                raw_response = response.json()[0]["generated_text"].strip()
                # Remove any part that repeats the question
                if question.lower() in raw_response.lower():
                    parts = raw_response.lower().split(question.lower())
                    raw_response = parts[-1].strip()
                return raw_response.strip()
            elif response.status_code == 503:
                time.sleep(RETRY_DELAY)
                continue
            else:
                response.raise_for_status()
                
        except Exception:
            if attempt == MAX_RETRIES - 1:
                raise HTTPException(status_code=503, detail="Service temporarily unavailable")
            time.sleep(RETRY_DELAY)
    
    raise HTTPException(status_code=503, detail="Service temporarily unavailable")

@app.post("/api/")
async def answer_question(
    question: str = Form(...),
    model: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        # Handle file if provided
        if file:
            try:
                # Read the uploaded ZIP file
                zip_content = await file.read()
                with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_ref:
                    # Check if ZIP file contains any files
                    if not zip_ref.namelist():
                        raise HTTPException(status_code=400, detail="ZIP file is empty")
                    
                    # Extract CSV file from ZIP
                    csv_filename = zip_ref.namelist()[0]
                    if not csv_filename.endswith('.csv'):
                        raise HTTPException(status_code=400, detail="No CSV file found in ZIP")
                    
                    with zip_ref.open(csv_filename) as csv_file:
                        df = pd.read_csv(csv_file)
                
                # Extract answer from CSV
                if 'answer' in df.columns:
                    if df.empty:
                        raise HTTPException(status_code=400, detail="CSV file is empty")
                    return {"answer": str(df['answer'].iloc[0])}
                else:
                    raise HTTPException(status_code=400, detail="Column 'answer' not found in CSV")
            except zipfile.BadZipFile:
                raise HTTPException(status_code=400, detail="Invalid ZIP file")
            except pd.errors.EmptyDataError:
                raise HTTPException(status_code=400, detail="CSV file is empty")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

        # Get LLM response
        llm_answer = get_llm_response(question, model)
        return {"answer": llm_answer}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List all available models."""
    return {
        "default_model": DEFAULT_MODEL,
        "available_models": list(MODELS.keys())
    }