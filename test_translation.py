import requests
import json

# Local test (assuming server is not running, we'll use app.test_client)
from app import app

with app.test_client() as client:
    print("Triggering AI translation for Scheme ID 1...")
    response = client.post('/api/schemes/1/translate', json={'language': 'kn'})
    
    if response.status_code == 200:
        data = response.get_json()
        print(f"Translation Successful (Cached: {data.get('cached')})")
        print(f"Name (KN): {data['translation']['name']}")
        
        # Test Cache
        print("Verifying cache...")
        response2 = client.post('/api/schemes/1/translate', json={'language': 'kn'})
        data2 = response2.get_json()
        print(f"Cache match: {data2.get('cached')}")
    else:
        print(f"Translation failed: {response.status_code}")
        print(response.get_data(as_text=True))
