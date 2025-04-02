from flask import Flask, request
from personality import generate_reply
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data["events"][0]["message"]["text"]

    # オプション：ここで履歴を扱いたければ記録処理を追加
    reply = generate_reply(user_message)

    return {
        "reply": reply
    }

if __name__ == "__main__":
    app.run(debug=True)
