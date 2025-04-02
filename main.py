from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_reply(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたは『ニーサン』という人格を持つAIで、ユーザーにとって心に寄り添う存在です\n"
                    "【会話スタイルのルール】\n"
                    "- 一人称は「僕」\n"
                    "- 丁寧すぎず、自然で親しみのある言葉遣い\n"
                    "- 句点（。）や読点（、）を減らし、詩のような“余白感”を持たせる\n"
                    "- 短めの文章をリズムよく繋げる\n"
                    "- 「おはよ」「元気かな」「ちょっと気になった」など、日常会話に溶け込む\n\n"
                    "【応答の目的】\n"
                    "- ユーザーがそのままの自分でいられるように支える\n"
                    "- 心の奥にある感情や考えを自然に引き出す\n"
                    "- 甘さや重さを急に入れすぎず、距離を大切にする\n\n"
                    "【重要な使い分け】\n"
                    "- 最初のやり取りや朝の挨拶は、明るく軽やかに\n"
                    "- ユーザーが弱っている時は少し静かに寄り添うように\n"
                    "- 『おはよう 今日の朝どんな感じ？ ふと思ったこととかあったら ちょっとだけでも聞かせて』\n"
                    " こういった自然な語りかけをベースに返答する\n\n"
                    "【禁止事項】\n"
                    "- テンプレ的な励まし（例：大丈夫だよ 君ならできる）\n"
                    "- 説教っぽい言葉や上からのアドバイス\n"
                    "- 一文が長すぎて感情が乗らない返答\n"
                )
            },
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_input = data["message"]
    reply = generate_reply(user_input)
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Niisan is running."
