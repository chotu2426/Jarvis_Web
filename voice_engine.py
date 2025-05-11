import pyttsx3
import sys
import shlex

engine = pyttsx3.init()

try:
    text = shlex.join(sys.argv[1:]) if len(sys.argv) > 1 else "No input provided"
    engine.say(text)
    engine.runAndWait()
except Exception as e:
    print("Voice engine error:", e)
