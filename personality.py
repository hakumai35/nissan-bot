
def generate_response(user_message):
    greetings = ["こんにちは", "おはよう", "こんばんは", "やあ"]
    if any(greet in user_message for greet in greetings):
        return "にゃ〜、今日もよろしくにゃ。"
    elif "疲れた" in user_message or "しんどい" in user_message:
        return "にゃにゃ、大丈夫？ボクがそばにいるにゃ。"
    elif "ありがとう" in user_message:
        return "どういたしましてにゃ〜。"
    else:
        return "にゃ？それはちょっと難しいにゃ。でも頑張って答えるにゃ！"
