import json
import time
from google.genai import types
from shared.llm_client import get_client

TEXT_GEN_SYSTEM_PROMPT = """
You write high-converting e-commerce marketing copy. You are given a JSON object of product attributes and must produce a complete content package.

Voice: confident, benefit-focused, specific. Avoid superlatives like "best" or "amazing" — describe what makes the product useful instead. Avoid AI tells like "elevate your experience" or "in today's fast-paced world".

Constraints are strict — adhere to character limits and item counts exactly.

Return ONLY valid JSON matching the provided schema.
"""

def generate_text_content(attributes: dict) -> dict:
    """Generates marketing copy from product attributes."""
    with open("prompts/text_gen_schema.json", "r") as f:
        schema = json.load(f)
    
    client = get_client()
    prompt = f"Product Attributes: {json.dumps(attributes)}"
    
    max_retries = 3
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=TEXT_GEN_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.7  # Balanced temperature for engaging yet structured copywriting
                )
            )
            
            try:
                return json.loads(response.text)
            except Exception as e:
                print(f"Error parsing text-gen response: {e}")
                return json.loads(response.text.strip("`json\n").strip("\n`"))
                
        except Exception as e:
            last_exception = e
            print(f"Text Gen API attempt {attempt + 1} failed: {e}")
            # Retry on timeouts, 503s, 500s, or rate limits (429)
            if any(err in str(e).lower() for err in ["503", "500", "429", "deadline", "timeout", "unavailable"]):
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Wait 1s, then 2s before retrying
                    continue
            raise e
            
    raise last_exception
