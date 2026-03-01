import asyncio
import edge_tts
import requests
import os

async def generate_test_audio():
    print("Generating test audio...")
    text = "What is the punishment for theft under Indian law?"
    communicate = edge_tts.Communicate(text, "en-IN-PrabhatNeural")
    await communicate.save("test_query.mp3")
    print("Test audio generated.")

async def main():
    await generate_test_audio()
    
    print("Sending POST request to /api/voice-query...")
    try:
        with open("test_query.mp3", "rb") as f:
            files = {"audio": ("test_query.mp3", f, "audio/mpeg")}
            response = requests.post("http://localhost:8000/api/voice-query", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response Data Keys:", data.keys())
            print("Transcript:", data.get("transcript"))
            print("Text Response:", data.get("text_response"))
            if data.get("audio_base64"):
                print("Audio Base64 length:", len(data.get("audio_base64")))
            if data.get("error"):
                print("Error from API:", data.get("error"))
        else:
            print("Failed to get a successful response:", response.text)
    except Exception as e:
        print("Exception during request:", str(e))
    finally:
        if os.path.exists("test_query.mp3"):
            os.remove("test_query.mp3")

if __name__ == "__main__":
    asyncio.run(main())
