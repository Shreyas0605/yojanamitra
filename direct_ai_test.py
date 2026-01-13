import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print(f"Testing key: {key[:10]}...")

try:
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-pro-latest')
    response = model.generate_content("Translate 'Hello' to Kannada")
    print(f"✅ Success: {response.text}")
except Exception as e:
    print(f"❌ Failed: {str(e)}")
