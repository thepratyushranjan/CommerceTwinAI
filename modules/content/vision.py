import json
import io
import time
import PIL.Image
from google.genai import types
from shared.llm_client import get_client

VISION_SYSTEM_PROMPT = """
You are a product analyst extracting structured attributes from product images for an e-commerce catalog. 
Be specific and concrete. Avoid generic adjectives like "nice" or "good quality". 
Focus on visually-verifiable attributes only. 
If you cannot determine a field with confidence, make a best estimate based on visible evidence rather than leaving it blank.

Return ONLY valid JSON matching the provided schema.
"""

def analyze_image(image_bytes: bytes) -> dict:
    """Analyzes a product image with automatic fallback and retries for stability."""
    with open("prompts/vision_schema.json", "r") as f:
        schema = json.load(f)
    
    client = get_client()
    img = PIL.Image.open(io.BytesIO(image_bytes))
    
    # We try Pro first, then fallback to Flash if Pro is unavailable/timing out
    models_to_try = ['gemini-2.5-pro', 'gemini-2.5-flash']
    
    last_exception = None
    
    for model_name in models_to_try:
        max_retries = 2
        for attempt in range(max_retries):
            try:
                print(f"Attempting vision analysis with {model_name} (Attempt {attempt + 1})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=["Analyze this product image and return attributes in JSON format.", img],
                    config=types.GenerateContentConfig(
                        system_instruction=VISION_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=schema,
                        temperature=0.1 # Very low for maximum factual accuracy
                    )
                )
                
                try:
                    return json.loads(response.text)
                except Exception as e:
                    # Fallback string cleaning if JSON mode has a minor hiccup
                    cleaned_text = response.text.strip().strip("```json").strip("```").strip()
                    return json.loads(cleaned_text)
                    
            except Exception as e:
                last_exception = e
                error_msg = str(e).lower()
                print(f"Vision API error with {model_name}: {e}")
                
                # If it's a 503/Timeout, we retry or switch model
                if any(err in error_msg for err in ["503", "500", "429", "deadline", "timeout", "unavailable"]):
                    if attempt < max_retries - 1:
                        time.sleep(3) # Wait 3 seconds before retry
                        continue
                    else:
                        print(f"Switching from {model_name} due to persistent errors...")
                        break # Break retry loop to try next model
                else:
                    # For other errors (like 400 Bad Request), don't bother retrying
                    raise e
                    
    print("All vision models failed. Raising last exception.")
    raise last_exception
