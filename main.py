from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from personality import get_response

app = Flask(__name__)

# 環境変数から取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

# チェック
if LINE_CHANNEL_ACCESS_TOKEN is None or LINE_CHANNEL_SECRET is None:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN または LINE_CHANNEL_SECRET が未設定です。")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def index():
    return "にゃ〜ん、LINE Botはちゃんと動いてるにゃ。"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    print("[LOG] Webhook受信")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("[ERROR] シグネチャ不一致")
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print(f"[LOG] ユーザーからのメッセージ: {user_message}")

    try:
        reply = get_response(user_message)
        print(f"[LOG] 返信内容: {reply}")
    except Exception as e:
        print(f"[ERROR] get_response内でエラー: {e}")
        reply = "今ちょっと調子が悪いみたい…また話しかけてにゃ。"

    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except Exception as e:
        print(f"[ERROR] LINE返信時のエラー: {e}")

# Renderでは gunicorn が起動するので app.run() は不要
# ローカル開発用に使いたい場合だけ有効化してね
# if __name__ == "__main__":
#     app.run()
