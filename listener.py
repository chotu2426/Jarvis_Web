import speech_recognition as sr
import requests
import subprocess
import shlex
import time

WAKE_WORD = "jarvis"

def speak(text):
    safe_text = shlex.quote(text)
    subprocess.run(["python", "voice_engine.py", safe_text])

def listen_for_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎙 Listening for command...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"👉 Command: {command}")
        # Send the command to the Flask app
        response = requests.post("http://127.0.0.1:5000/process", json={"command": command})
        print("💬 Jarvis:", response.json().get("response", "No response."))
    except sr.UnknownValueError:
        print("🙁 Didn't understand the command.")
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        print("⚠️ Speech Recognition service error.")
        speak("Speech service error occurred.")

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("👂 Listening for wake word...")

        while True:
            try:
                audio = recognizer.listen(source)
                phrase = recognizer.recognize_google(audio).lower()
                print(f"🎧 Heard: {phrase}")
                if WAKE_WORD in phrase:
                    print("✅ Wake word detected.")
                    speak("Yes, how can I help?")
                    listen_for_command()
                    time.sleep(1)  # Brief pause before listening again
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print("⚠️ API unavailable:", e)
                speak("Internet connection issue.")
                time.sleep(5)

if __name__ == "__main__":
    listen_for_wake_word()
