from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

from responder import generate_niisan_reply

app = Flask(__name__)

# 環境変数からトークンを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route('/')
def home():
    return 'Bot is running'

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    reply = generate_niisan_reply(user_id, user_message)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == '__main__':
    app.run()
