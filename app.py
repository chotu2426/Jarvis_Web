from flask import Flask, render_template, request, session
from flask_session import Session
import datetime
import wikipedia
import pyjokes
import webbrowser

app = Flask(__name__)
app.secret_key = "secret-key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def respond_to_command(command):
    command = command.lower()

    if "time" in command:
        return datetime.datetime.now().strftime("The current time is %I:%M %p")

    elif "date" in command:
        return datetime.datetime.now().strftime("Today is %A, %d %B %Y")

    elif "joke" in command:
        return pyjokes.get_joke()

    elif "wikipedia" in command:
        try:
            topic = command.replace("wikipedia", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            return f"According to Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Your query is too vague. Did you mean: {', '.join(e.options[:5])}?"
        except wikipedia.exceptions.PageError:
            return "Sorry, that Wikipedia page doesn't exist."
        except Exception:
            return "Sorry, I couldn't fetch that Wikipedia article."

    elif "search" in command:
        query = command.replace("search", "").strip()
        return f"<a href='https://www.google.com/search?q={query}' target='_blank'>Search Google for {query}</a>"

    elif "weather" in command:
        city = command.replace("weather", "").strip()
        return f"<a href='https://www.google.com/search?q=weather+{city}' target='_blank'>Check weather in {city}</a>"

    else:
        return "Sorry, I don't understand that command."

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    response = ""
    if request.method == "POST":
        user_input = request.form["command"]
        response = respond_to_command(user_input)
        session["history"].append((user_input, response))
        session.modified = True

    return render_template("index.html", response=response, history=session["history"])

if __name__ == "__main__":
    app.run(debug=True)
