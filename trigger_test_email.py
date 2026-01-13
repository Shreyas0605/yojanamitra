import requests
import time

def trigger_test():
    print("Triggering Test Email via API...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/test-email-system')
        print(f"Status Code: {response.status_code}")
        try:
            print("Response:", response.json())
        except:
            print("Response Text:", response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")
        print("Ensure server is running!")

if __name__ == "__main__":
    trigger_test()
