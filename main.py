from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from personality import generate_reply
import os

app = Flask(__name__)

# 環境変数からチャンネルアクセストークンとシークレットを取得
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    except Exception as e:
        print("Webhook error:", e)
        return "Error", 500
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_input = event.message.text
        reply_text = generate_reply(user_input)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    except Exception as e:
        print("Handle message error:", e)
