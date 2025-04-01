from personality import generate_reply
from memory import get_history, update_history
from datetime import datetime
import pytz

MAX_HISTORY = 10
TIMEZONE = pytz.timezone('Asia/Tokyo')

def generate_niisan_reply(user_id, user_message):
    now = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")

    # ユーザー履歴を取得
    history = get_history(user_id)

    # 履歴が多すぎる場合、古いものから削除
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    # 会話履歴に現在のユーザー入力を追加
    history.append({"role": "user", "content": user_message})

    # AIからの応答生成
    reply = generate_reply(history)

    # 履歴にAIの応答も追加
    history.append({"role": "assistant", "content": reply})

    # 最新履歴を保存
    update_history(user_id, history)

    return reply
