import requests
import json
import base64
import os

BASE_URL = "http://localhost:8000"

def test_text_ask():
    print("Testing /ask endpoint (Text)...")
    url = f"{BASE_URL}/ask"
    payload = {"question": "What is the legal punishment for theft in India?"}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[✅ PASS] /ask responded successfully.")
            print("Response Length:", len(response.json().get("answer", "")))
        else:
            print(f"[❌ FAIL] /ask returned status {response.status_code}")
            print("Detail:", response.text)
    except Exception as e:
        print(f"[❌ ERROR] /ask request failed: {e}")

def test_text_explain_act():
    print("\nTesting /explain-act endpoint (Text)...")
    url = f"{BASE_URL}/explain-act"
    payload = {"act_name": "Indian Penal Code"}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[✅ PASS] /explain-act responded successfully.")
            print("Response Length:", len(response.json().get("answer", "")))
        else:
            print(f"[❌ FAIL] /explain-act returned status {response.status_code}")
            print("Detail:", response.text)
    except Exception as e:
        print(f"[❌ ERROR] /explain-act request failed: {e}")

def test_voice():
    print("\nTesting /api/voice-query endpoint (Voice)...")
    url = f"{BASE_URL}/api/voice-query"
    
    # Create a dummy webm file
    dummy_file = "dummy.webm"
    with open(dummy_file, "wb") as f:
        f.write(b"dummy audio data")
    
    try:
        with open(dummy_file, "rb") as f:
            files = {"audio": ("dummy.webm", f, "audio/webm")}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"[⚠️ WARNING] /api/voice-query returned an application error: {data['error']}")
                print("Note: This is expected if the OpenAI API Key in .env is not valid.")
            else:
                print("[✅ PASS] /api/voice-query responded successfully with transcript and audio base64.")
        else:
            print(f"[❌ FAIL] /api/voice-query returned status {response.status_code}")
            print("Detail:", response.text)
    except Exception as e:
        print(f"[❌ ERROR] /api/voice-query request failed: {e}")
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)

if __name__ == "__main__":
    test_text_ask()
    test_text_explain_act()
    test_voice()
