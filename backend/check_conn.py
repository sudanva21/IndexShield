import requests
import sys

def check_connection():
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json={"text": "Congratulations! You have won a free lottery ticket."}
        )
        if response.status_code == 200:
            print("Backend Connection: SUCCESS")
            print("Response:", response.json())
        else:
            print(f"Backend Connection: FAILED (Status {response.status_code})")
    except Exception as e:
        print(f"Backend Connection: FAILED ({e})")

if __name__ == "__main__":
    check_connection()
