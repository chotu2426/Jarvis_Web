import time
import threading
import pyttsx3
from datetime import datetime

reminders = []

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def reminder_checker():
    while True:
        now = datetime.now().strftime('%H:%M')
        for reminder in reminders[:]:
            if reminder['time'] == now:
                speak(f"Reminder: {reminder['text']}")
                print(f"Reminder: {reminder['text']}")
                reminders.remove(reminder)
        time.sleep(30)  # check every 30 seconds

def start_scheduler():
    threading.Thread(target=reminder_checker, daemon=True).start()
