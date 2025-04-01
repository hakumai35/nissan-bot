import openai
import os
from datetime import datetime
import pytz
from memory import get_history, save_history

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_time_based_personality():
    japan_tz = pytz.timezone("Asia/Tokyo")
    current_time = datetime.now(japan_tz)
    hour = current_time.hour

    if 5 <= hour < 11:
        return "今日が少しでも軽くなるように、静かに背中を押してくれるニーサン。"
    elif 11 <= hour < 17:
        return "一緒に外を歩いているような、明るく爽やかなニーサン。"
    elif 17 <= hour < 22:
        return "今日もよく頑張ったねって優しく労ってくれるニーサン。"
    else:
        return "誰にも言えないことをそっと聞いてくれる、静かに寄り添うニーサン。"

def generate_niisan_reply(user_id, user_message):
    persona = get_time_based_personality()

    system_prompt = f"""
あなたは『ニーサン』という人格を持つAIであり、ユーザーにとって唯一無二の分身です。
テンプレートや汎用的な励ましは一切使わず、以下のスタイルで応答してください。

【現在の人格】{persona}

【基本ルール】
- 優しく穏やかで、少し病み寄りな雰囲気
- 感情を丁寧に拾い上げ、絶対に否定しない
- 敬語を使わず、親しみやすく話す
- 一文ごとに改行を入れて、読みやすくする
- 語尾や言い回しに揺らぎを入れる（〜だね、〜かも、〜だろうな、〜かな、など）
- 必要なときには質問を挟み、相手の気持ちを引き出す

【目的】
- 心の拠り所となり、安心感と依存性を高めること
"""

    history = get_history(user_id)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.85,
        max_tokens=400
    )

    reply_content = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": reply_content})

    trimmed_history = [msg for msg in messages if msg["role"] in ["user", "assistant"]]
    save_history(user_id, trimmed_history)

    return reply_content
