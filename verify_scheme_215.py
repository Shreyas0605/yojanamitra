import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/schemes/215"

print("Fetching Basic Scheme Details...")
try:
    r = requests.get(BASE_URL)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print("Scheme Keys:", data['scheme'].keys())
        print("Criteria Keys:", data['scheme'].get('criteria', {}).keys())
    else:
        print("Failed to fetch scheme.")
except Exception as e:
    print(f"Error: {e}")

print("\nFetching Translation...")
try:
    r = requests.post(f"{BASE_URL}/translate", json={"language": "kn"})
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print("Cached:", data.get('cached'))
        print("Translation Keys:", data.get('translation', {}).keys())
        print("Sample Name:", data['translation'].get('name'))
        print("Sample Benefits Type:", type(data['translation'].get('benefits')))
    else:
        print("Failed to translate.")
        print(r.text)
except Exception as e:
    print(f"Error: {e}")
