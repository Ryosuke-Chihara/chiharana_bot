from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import re
import os
import dotenv

app = Flask(__name__)

# LINEのチャネル設定
dotenv.load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# パターンと返信メッセージの辞書
patterns = {
    "keywords": ([
        r'千原', r'茅原', r'苑原', r'田原', r'地腹', r'血はら'
    ], "地原な。"),
    "hey": ([r'やっほ', r'ヤッホ'], "やっほー。"),
    "good_morning": ([r'おはよ'], "おはよう。"),
    "hello": ([r'こんにち', r'こんちは', r'こんちわ', r'こんちゃ'], "こんにちは。"),
    "good_evening": ([r'こんばん'], "こんばんは。"),
}

@app.route("/")
def hello_world():
    return "hello world!"

# Webhookエンドポイント
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def match_reply(user_message, patterns):
    for pattern_list, reply in patterns.values():
        if any(re.search(p, user_message, re.IGNORECASE) for p in pattern_list):
            return reply
    return

# メッセージイベントの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_message = match_reply(user_message, patterns)
    
    if reply_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
