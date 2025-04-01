import redis
import os
import json

REDIS_URL = os.environ.get("REDIS_URL")
r = redis.from_url(REDIS_URL)

def get_history(user_id):
    key = f"history:{user_id}"
    history_json = r.get(key)
    if history_json is None:
        return []
    return json.loads(history_json)

def save_history(user_id, messages):
    key = f"history:{user_id}"
    if len(messages) > 10:
        messages = messages[-10:]
    r.set(key, json.dumps(messages))
