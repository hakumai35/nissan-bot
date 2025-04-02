from flask import Flask, request, jsonify
from personality import generate_reply
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # 安全チェックを入れる
    try:
        events = data.get("events", [])
        if not events or "message" not in events[0] or "text" not in events[0]["message"]:
            return jsonify({"status": "ignored"}), 200

        user_message = events[0]["message"]["text"]
        reply = generate_reply(user_message)
        return jsonify({"reply": reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
