import os
import io
import json
from PIL import Image
from modules.content.vision import analyze_image
from modules.content.text_gen import generate_text_content
from modules.content.banner import generate_banner

def create_test_image():
    # Create a simple red square image for testing
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def test_pipeline():
    print("🚀 Starting Content Generator Pipeline Test...")
    
    # 1. Create test image
    image_bytes = create_test_image()
    print("✅ Created test image.")
    
    try:
        # 2. Test Vision Analysis
        print("📸 Testing Vision Analysis (Gemini 2.5 Pro)...")
        attributes = analyze_image(image_bytes)
        print("✅ Vision Attributes:", json.dumps(attributes, indent=2))
        
        # 3. Test Text Generation
        print("\n📝 Testing Text Generation (Gemini 2.5 Flash)...")
        text_content = generate_text_content(attributes)
        print("✅ Text Content:", json.dumps(text_content, indent=2))
        
        # 4. Test Banner Generation
        print("\n🖼️ Testing Banner Generation (Pollinations.ai + PIL)...")
        banner_bytes = generate_banner(attributes, text_content.get("title", "Test Product"))
        if banner_bytes:
            print(f"✅ Banner generated successfully ({len(banner_bytes)} bytes)")
            with open("data/test_banner.png", "wb") as f:
                f.write(banner_bytes)
            print("📁 Saved test banner to data/test_banner.png")
            
        print("\n✨ ALL BACKEND TESTS PASSED!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    test_pipeline()
