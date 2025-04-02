from flask import Flask, request, jsonify
from personality import generate_reply

app = Flask(__name__)

@app.route("/")
def index():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        event = data["events"][0]
        user_input = event["message"]["text"]
    except (KeyError, IndexError):
        return jsonify({"error": "Invalid message format"}), 400

    reply = generate_reply(user_input)
    return jsonify({"reply": reply})
