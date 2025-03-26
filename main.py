import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Use environment variable instead of hardcoded token
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY environment variable is not set")