from flask import Flask, render_template, request, jsonify
import datetime
import psutil
import os
import webbrowser
import threading
import time
import requests
import subprocess
import shlex

app = Flask(__name__)
todos = []
reminders = []

# ✅ Speak via subprocess to avoid run loop error
def speak(text):
    try:
        safe_text = shlex.quote(text)
        subprocess.run(["python", "voice_engine.py", safe_text])
    except Exception as e:
        print("Error in speaking:", e)

# ✅ Background thread to check reminders
def reminder_checker():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for reminder in reminders:
            if reminder['time'] == now and not reminder['notified']:
                speak(f"Reminder: {reminder['text']}")
                reminder['notified'] = True
        time.sleep(30)

threading.Thread(target=reminder_checker, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reminders", methods=["GET", "POST"])
def handle_reminders():
    if request.method == "POST":
        data = request.get_json()
        text = data["text"]
        time_str = data["time"]
        reminders.append({"text": text, "time": time_str, "notified": False})
        return jsonify({"message": "Reminder added"})
    else:
        return jsonify({"reminders": reminders})

@app.route("/reminders/<int:index>", methods=["DELETE"])
def delete_reminder(index):
    if 0 <= index < len(reminders):
        del reminders[index]
    return jsonify({"message": "Reminder deleted"})

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    command = data.get("command", "").lower()
    response = ""

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The time is {now}."

    elif "battery" in command:
        battery = psutil.sensors_battery()
        response = f"Battery is at {battery.percent}%"

    elif "screenshot" in command:
        try:
            import pyautogui
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = f"screenshot_{timestamp}.png"
            pyautogui.screenshot(file_path)
            response = "Screenshot taken and saved."
        except:
            response = "Failed to take screenshot."

    elif "open" in command:
        app_name = command.replace("open", "").strip()
        if "notepad" in app_name:
            subprocess.Popen(["notepad.exe"])
            response = "Opening Notepad"
        elif "spotify" in app_name:
            spotify_path = "C:/Users/YourUsername/AppData/Roaming/Spotify/Spotify.exe"  # Replace path
            if os.path.exists(spotify_path):
                os.startfile(spotify_path)
                response = "Opening Spotify"
            else:
                response = "Spotify not found"
        elif "youtube" in app_name:
            webbrowser.open("https://www.youtube.com")
            response = "Opening YouTube"
        else:
            response = f"Trying to open {app_name}"
            os.system(f"start {app_name}")

    elif "remind me to" in command:
        try:
            note = command.split("remind me to")[1].split("at")[0].strip()
            time_str = command.split("at")[-1].strip()
            reminders.append({"text": note, "time": time_str, "notified": False})
            response = f"Reminder set for {note} at {time_str}"
        except:
            response = "Sorry, I couldn't set the reminder."

    elif "note" in command:
        note = command.replace("note", "").strip()
        todos.append(note)
        response = f"Noted: {note}"

    elif "weather" in command:
        api_key = "your_openweathermap_api_key"  # Replace
        city = "your_city"  # Replace
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url).json()
        if r.get("main"):
            temp = r['main']['temp']
            desc = r['weather'][0]['description']
            response = f"Current temperature in {city} is {temp}°C with {desc}."
        else:
            response = "Sorry, I couldn't fetch the weather."

    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        response = f"Searching Google for {query}"

    elif "play" in command:
        song = command.replace("play", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        response = f"Playing {song} on YouTube"

    elif "joke" in command:
        try:
            joke_res = requests.get("https://official-joke-api.appspot.com/jokes/random").json()
            setup = joke_res.get("setup", "")
            punchline = joke_res.get("punchline", "")
            response = f"Here's a joke: {setup} ... {punchline}"
        except:
            response = "Sorry, I couldn't fetch a joke."

    else:
        response = "Sorry, I didn't understand."

    speak(response)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
