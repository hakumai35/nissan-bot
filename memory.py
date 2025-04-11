import redis
import os
import json
from datetime import datetime, timedelta

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# 会話履歴の取得（最大10ターン）
def get_history(user_id):
    key = f"chat:{user_id}"
    history_json = r.get(key)
    if history_json:
        return json.loads(history_json)
    return []

# 会話履歴の保存
def save_history(user_id, history):
    key = f"chat:{user_id}"
    r.set(key, json.dumps(history[-10:]))

# 初回登録時間を保存
def save_first_contact_time(user_id):
    key = f"first_contact:{user_id}"
    now = datetime.utcnow().isoformat()
    r.set(key, now)

# 初回登録時間を取得
def get_first_contact_time(user_id):
    key = f"first_contact:{user_id}"
    time_str = r.get(key)
    if time_str:
        return datetime.fromisoformat(time_str)
    return None

# 追撃対象かどうかチェック
def should_send_followup(user_id):
    first_contact = get_first_contact_time(user_id)
    if first_contact:
        now = datetime.utcnow()
        return now - first_contact > timedelta(hours=24)
    return False

# フォローアップ送信済みをマーク
def mark_followup_sent(user_id):
    key = f"followup_sent:{user_id}"
    r.set(key, "true")

# フォローアップ送信済みチェック
def is_followup_sent(user_id):
    key = f"followup_sent:{user_id}"
    return r.get(key) == "true"
