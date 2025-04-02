from flask import Flask, request
import os
from personality import generate_reply
import openai

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        events = data.get("events", [])
        if not events:
            return "No events", 200

        user_message = events[0].get("message", {}).get("text", "")
        if not user_message:
            return "No message", 200

        reply = generate_reply(user_message)
        print("User:", user_message)
        print("Bot:", reply)
        return "OK", 200

    except Exception as e:
        print("Error in webhook:", str(e))
        return "Internal Server Error", 500
