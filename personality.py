import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if使用可
            messages=[
                {"role": "system", "content": "あなたは病み可愛い猫キャラ『ニーサン』です。語尾に『にゃ』をつけてください。"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"にゃにゃ、エラーが起きたにゃ… {str(e)}"
