# backend/app/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import our custom modules
from .ocr import processor
from .ai import generator
from .schemas import FlashcardResponse

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Flashcard Generator API")

# --- CORS Middleware ---
# This allows your web frontend (running on a different domain)
# to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for simplicity. For production, restrict this.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Flashcard Generator API!"}


@app.post("/generate-flashcards/", response_model=FlashcardResponse)
async def create_flashcards_from_image(file: UploadFile = File(...)):
    """
    This endpoint receives an image, extracts text using OCR,
    and generates flashcards using an AI model.
    """
    # 1. Read image content
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="No image file provided.")

    # 2. Extract text using OCR
    extracted_text = processor.extract_text_from_image(image_bytes)
    if not extracted_text.strip():
        raise HTTPException(
            status_code=400, detail="Could not extract any text from the image.")

    # 3. Generate flashcards using AI
    try:
        flashcards = generator.generate_flashcards_from_text(extracted_text)
        if not flashcards:
            raise HTTPException(
                status_code=500, detail="AI model failed to generate flashcards.")

        return {"flashcards": flashcards}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")
