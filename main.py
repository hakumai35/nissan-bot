from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境変数（Render では Dashboard から設定）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ルート確認用
@app.route('/')
def index():
    return 'Bot is alive'

# Webhook エンドポイント
@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# イベントハンドラー
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply = generate_reply(user_message)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# 簡易応答生成関数（ここは後でチューニング可能）
def generate_reply(message):
    return f"あなたの言葉『{message}』、ちゃんと受け取ったよ。"

if __name__ == "__main__":
    app.run()
