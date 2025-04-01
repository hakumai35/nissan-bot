from personality import generate_reply
from memory import get_history, save_history

def generate_niisan_reply(user_id, user_message):
    history = get_history(user_id)
    history.append({"role": "user", "content": user_message})
    reply = generate_reply(history)
    history.append({"role": "assistant", "content": reply})
    save_history(user_id, history)
    return reply
