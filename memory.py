import redis
import json
import os

r = redis.from_url(os.environ["REDIS_URL"])

def get_history(user_id):
    key = f"history:{user_id}"
    history_json = r.get(key)
    if history_json:
        return json.loads(history_json)
    return []

def save_history(user_id, user_msg, reply_msg):
    key = f"history:{user_id}"
    history = get_history(user_id)
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": reply_msg})
    r.set(key, json.dumps(history[-10:]))  # 最新10件のみ保存
