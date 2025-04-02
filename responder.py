# responder.py
import openai
import os
from datetime import datetime
import pytz
from memory import get_history, save_history
from personality import get_personality_prompt

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_niisan_reply(user_id, user_message):
    system_prompt = get_personality_prompt()

    history = get_history(user_id)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.88,
        max_tokens=600
    )

    reply_content = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": reply_content})

    trimmed_history = [msg for msg in messages if msg["role"] in ["user", "assistant"]][-10:]
    save_history(user_id, trimmed_history)

    return reply_content
