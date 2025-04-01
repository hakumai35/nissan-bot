import os
from openai import OpenAI
from memory import get_history, save_history
from personality import generate_niisan_reply as persona_reply

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_niisan_reply(user_id, user_input):
    history = get_history(user_id)
    
    messages = history + [
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    ai_reply = response.choices[0].message.content.strip()

    # 履歴に保存
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": ai_reply})
    save_history(user_id, history[-10:])  # 最新10件だけ保存

    return ai_reply
