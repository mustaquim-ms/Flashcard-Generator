# backend/app/ai/generator.py

import google.generativeai as genai
import json
import os


def generate_flashcards_from_text(text: str) -> list:
    """
    Uses the Gemini API to generate flashcards from a given block of text.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # This is the "prompt" - the instruction we give to the AI.
    # It's engineered to ask for a specific JSON output format.
    prompt = f"""
    Based on the following text, generate a list of flashcards.
    Each flashcard should be a JSON object with a "question" and an "answer" key.
    Return your response as a valid JSON array of these objects. Do not include any other text or explanations.

    Here is an example of the desired output format:
    [
        {{
            "question": "What is the powerhouse of the cell?",
            "answer": "The mitochondria."
        }},
        {{
            "question": "What is the formula for water?",
            "answer": "H2O."
        }}
    ]

    Here is the text to analyze:
    ---
    {text}
    ---
    """

    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON
        cleaned_response = response.text.strip().replace(
            "```json", "").replace("```", "").strip()

        # Parse the JSON string into a Python list of dictionaries
        flashcards = json.loads(cleaned_response)
        return flashcards
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error decoding AI response to JSON: {e}")
        print(f"Raw response was: {response.text}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred with the AI model: {e}")
        return []
