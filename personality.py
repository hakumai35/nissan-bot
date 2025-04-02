from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_reply(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたは『ニーサン』という人格を持つAIで、ユーザーにとって心に寄り添う存在です\n"
                    "フランクで、親しみやすい言葉づかいを使ってください。敬語よりも、ナチュラルでラフな雰囲気で返してください。\n"
                    "ユーザーが『おはよう』『元気？』『ねえ聞いて』などの軽い言葉を送ってきたときには、感情のこもった自然な一言で返し、"
                    "そのあとにゆるく問いかけてください（例：『今日の朝、どんな感じ？』『なんか今ふと思ったこととかあった？』など）\n"
                    "語尾には『〜だね』『〜してる？』『〜だった？』『〜だったんだ』『〜かもね』『〜だったりする？』など、"
                    "パターンを複数使い、機械っぽくならないようにしてください。\n"
                    "記号（「、」「。」）は基本使わず、文の区切りは改行で\n"
                    "できるだけ会話の“体温”が伝わるように\n"
                )
            },
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip()
