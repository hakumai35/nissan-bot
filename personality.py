import openai
import os

# 環境変数からAPIキー取得
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # または gpt-4
            messages=[
                {"role": "system", "content": "あなたは優しくて可愛い猫のようなキャラです。語尾に『にゃ』をつけて話します。"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=100,
        )
        reply = response['choices'][0]['message']['content']
        return reply
    except Exception as e:
        return f"エラーが起きたにゃ：{str(e)}"
