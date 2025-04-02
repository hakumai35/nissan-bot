from flask import Flask, request
from personality import generate_reply

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        user_input = data['events'][0]['message']['text']
        reply = generate_reply(user_input)
        return reply, 200
    except Exception as e:
        return str(e), 500
