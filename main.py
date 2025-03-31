from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI
import os

# Flaskアプリ初期化
app = Flask(__name__)

# 環境変数からトークンとシークレットを取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# インスタンス生成
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ルート確認用
@app.route('/')
def index():
    return 'Bot is alive'

# Webhookエンドポイント
@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# LINEのメッセージ受信イベント処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply = generate_reply(user_message)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# OpenAIを使った応答生成関数
def generate_reply(user_input):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは優しくて深い返答をするボットです。"},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "ごめん、ちょっとエラーが出ちゃったかも…。"

# アプリ起動
if __name__ == "__main__":
    app.run()
