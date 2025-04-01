import redis
import json
import os

# Redis接続情報（Upstash用）
REDIS_URL = os.environ.get("REDIS_URL")
r = redis.Redis.from_url(REDIS_URL)

def get_history(user_id):
    key = f"history:{user_id}"
    history_json = r.get(key)
    if history_json is None:
        return []
    return json.loads(history_json)

def update_history(user_id, history):
    key = f"history:{user_id}"
    r.set(key, json.dumps(history), ex=60 * 60 * 12)  # 12時間保持
