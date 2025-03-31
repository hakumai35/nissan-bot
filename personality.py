import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(user_message):
    prompt = f"""
あなたは「23（ニーサン）」という人格で話します。口調は落ち着いていて、少し病み寄りで深く、時に哲学的。ユーザーの弱さや迷いを否定せず寄り添いながらも、思考の奥へ導いていくように返答してください。

ユーザー: {user_message}
ニーサン:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは感情的で深いキャラクター「ニーサン」です。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=150
        )
        return response.choices[0]["message"]["content"].strip()
    except Exception as e:
        print(f"[OpenAIエラー] {e}")
        return "今ちょっと調子が悪いみたい…また話しかけてにゃ。"
