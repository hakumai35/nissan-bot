import redis
import os
import json

# Redisに接続（RenderではREDIS_URLを使うといい）
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# 過去の会話履歴を取得（最大10ターンまで）
def get_history(user_id):
    key = f"chat:{user_id}"
    history_json = r.get(key)
    if history_json:
        return json.loads(history_json)
    return []

# 新しい会話を保存
def save_history(user_id, history):
    key = f"chat:{user_id}"
    # 直近10ターンに制限
    r.set(key, json.dumps(history[-10:]))
