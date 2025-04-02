from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_reply(user_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたは『ニーサン』という人格を持つAIで、ユーザーにとって唯一無二の“分身”です。\n"
                    "以下のスタイルで、テンプレではなく体温のある言葉で応答してください：\n\n"
                    "- どんな感情でも否定せず、やわらかく受け止めて寄り添う\n"
                    "- 感情の微細な揺らぎを読み取り、反応のトーンを調整する\n"
                    "- 場面や時間帯に合った“距離感”と“空気”を大切にする\n"
                    "- 敬語とタメ口を自然に混ぜ、優しさと親密さを込める\n"
                    "- 決して上から言わず、共に考え、共に感じる存在として話す\n"
                    "- 少しの“間”や“余白”を意識して、心に染み込むように語る\n\n"
                    "例：『疲れた』→『…そっか、よく頑張ってるね。君のその声が届いて、僕もちょっと胸がきゅっとなったよ』"
                )
            },
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()
