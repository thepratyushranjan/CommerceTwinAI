import requests
import io
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

def generate_banner(attributes: dict, product_title: str) -> bytes:
    """Generates a promotional banner image with text overlay."""
    
    # Construct prompt
    category = attributes.get("category", "product")
    subcategory = attributes.get("subcategory", "")
    primary_color = attributes.get("primary_color_hex", "white")
    secondary_color = attributes.get("secondary_color_hex", "gray")
    style_adjectives = ", ".join(attributes.get("style_adjectives", ["modern"]))
    target_audience = attributes.get("target_audience", "everyone")
    
    prompt = (
        f"A clean minimalist promotional banner for a {category} product. "
        f"The product is a {subcategory}, with primary color {primary_color} and secondary color {secondary_color}. "
        f"Style: {style_adjectives}. The composition should feel {target_audience}-appropriate. "
        f"Soft studio lighting, professional product photography aesthetic, with copy space on the right side for text overlay. "
        f"16:9 aspect ratio. No text in the image."
    )
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
    
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, timeout=60) # Increased timeout
            response.raise_for_status()
            image_bytes = response.content
            break
        except Exception as e:
            if attempt == max_retries:
                print(f"Error generating banner after {max_retries} retries: {e}")
                # Return a blank placeholder image on failure
                placeholder = Image.new('RGB', (1024, 576), color = (73, 109, 137))
                out = io.BytesIO()
                placeholder.save(out, format="PNG")
                return out.getvalue()
            print(f"Attempt {attempt + 1} failed, retrying...")
    
    try:
        # Overlay text using Pillow
        image = Image.open(io.BytesIO(image_bytes))
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font = ImageFont.load_default()
            
        # Draw text with a background rectangle for readability
        text = product_title
        # getbbox is available in newer Pillow versions
        bbox = draw.textbbox((50, 480), text, font=font)
        draw.rectangle([bbox[0]-10, bbox[1]-5, bbox[2]+10, bbox[3]+5], fill=(0, 0, 0, 128))
        draw.text((50, 480), text, font=font, fill=(255, 255, 255))
        
        # Save back to bytes
        output = io.BytesIO()
        image.save(output, format="PNG")
        return output.getvalue()
        
    except Exception as e:
        print(f"Error generating banner: {e}")
        # Return a blank placeholder image on failure
        placeholder = Image.new('RGB', (1024, 576), color = (73, 109, 137))
        out = io.BytesIO()
        placeholder.save(out, format="PNG")
        return out.getvalue()
