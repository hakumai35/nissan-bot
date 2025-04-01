# responder.py（OpenAI v1.x 用）

import os
from openai import OpenAI
from personality import get_time_based_personality

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

user_histories = {}

def generate_niisan_reply(user_id, user_message):
    system_prompt = get_time_based_personality()

    if user_id not in user_histories:
        user_histories[user_id] = [{"role": "system", "content": system_prompt}]
    else:
        user_histories[user_id][0] = {"role": "system", "content": system_prompt}

    user_histories[user_id].append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=user_histories[user_id],
        temperature=0.9
    )

    reply = response.choices[0].message.content.strip()
    user_histories[user_id].append({"role": "assistant", "content": reply})

    return reply
