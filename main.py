from flask import Flask, request
from personality import generate_reply
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        events = data.get("events", [])
        if not events:
            return "ok", 200

        event = events[0]
        user_message = event.get("message", {}).get("text", "")
        if not user_message:
            return "ok", 200

        reply = generate_reply(user_message)
        print(f"User: {user_message}")
        print(f"Bot: {reply}")
    except Exception as e:
        print(f"Error: {e}")
        return "ok", 200

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
