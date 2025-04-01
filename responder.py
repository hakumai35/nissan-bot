# responder.py

import openai
import os
from personality import get_time_based_personality

openai.api_key = os.getenv("OPENAI_API_KEY")

# ユーザーごとの会話履歴保存用
user_histories = {}

def generate_niisan_reply(user_id, user_message):
    system_prompt = get_time_based_personality()

    # 会話履歴取得 or 新規作成
    if user_id not in user_histories:
        user_histories[user_id] = [{"role": "system", "content": system_prompt}]
    else:
        # 毎回トーンを最新の時間帯で更新
        user_histories[user_id][0] = {"role": "system", "content": system_prompt}

    # ユーザー発言を履歴に追加
    user_histories[user_id].append({"role": "user", "content": user_message})

    # OpenAI APIに送信
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=user_histories[user_id],
        temperature=0.9
    )

    reply = response.choices[0].message["content"].strip()
    # AIの返答も履歴に追加
    user_histories[user_id].append({"role": "assistant", "content": reply})

    return reply
