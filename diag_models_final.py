import google.generativeai as genai
import os

# Use the Vault Key for diagnosis
key = "AIzaSyDKIs5LJqP5GW8BAJZbkXEDPtAOseI5IUo"
genai.configure(api_key=key)

print("--- DIAGNOSING AVAILABLE MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"MODEL: {m.name} | VERSION: {m.version if hasattr(m, 'version') else 'N/A'}")
except Exception as e:
    print(f"FAILED TO LIST MODELS: {e}")
