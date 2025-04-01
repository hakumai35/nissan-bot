import redis
import json
import os

r = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)

def get_history(user_id):
    key = f"history:{user_id}"
    history_json = r.get(key)
    if history_json:
        return json.loads(history_json)
    else:
        return []

def save_history(user_id, history):
    key = f"history:{user_id}"
    r.set(key, json.dumps(history))
