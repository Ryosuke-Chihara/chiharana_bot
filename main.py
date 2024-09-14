from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import re
import os, dotenv

app = Flask(__name__)

# LINEのチャネル設定
dotenv.load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN =  os.environ["CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 部分一致を確認する正規表現のリスト
keywords = [
    re.compile(r'千原', re.IGNORECASE),
    re.compile(r'ちはら', re.IGNORECASE),
    re.compile(r'茅原', re.IGNORECASE),
    re.compile(r'苑原', re.IGNORECASE),
    re.compile(r'chihara', re.IGNORECASE),
    re.compile(r'tihara', re.IGNORECASE),
    re.compile(r'チハラ', re.IGNORECASE),
    re.compile(r'田原', re.IGNORECASE),
    re.compile(r'地腹', re.IGNORECASE),
    re.compile(r'血はら', re.IGNORECASE),
    re.compile(r'ちんちん', re.IGNORECASE),
    re.compile(r'チンチン', re.IGNORECASE),
]
thanks = [
    re.compile(r'さんきゅ', re.IGNORECASE),
    re.compile(r'サンキュ', re.IGNORECASE),
    re.compile(r'thank', re.IGNORECASE),
    re.compile(r'ありがと', re.IGNORECASE),
]
hey = [
    re.compile(r'やっほ', re.IGNORECASE),
    re.compile(r'ヤッホ', re.IGNORECASE),
]
good_morning = [
    re.compile(r'おはよ', re.IGNORECASE),
]
hello = [
    re.compile(r'こんにち', re.IGNORECASE),
]
good_evening = [
    re.compile(r'こんばん', re.IGNORECASE),
]
good_night = [
    re.compile(r'おやす', re.IGNORECASE),
]

@app.route("/")
def hello_world():
    return "hello world!"

# Webhookエンドポイント
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# メッセージイベントの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 正規表現で部分一致をチェック
    match = any(pattern.search(user_message) for pattern in keywords)

    if match:
        # 一致した場合、「地原な。」と返信
        reply_message = "地原な。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return

    match = any(pattern.search(user_message) for pattern in thanks)
    if match:
        # 一致した場合、「どういたしまして」と返信
        reply_message = "どういたしまして。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return

    match = any(pattern.search(user_message) for pattern in hey)
    if match:
        # 一致した場合、「やっほー」と返信
        reply_message = "やっほー。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return

    match = any(pattern.search(user_message) for pattern in good_morning)
    if match:
        # 一致した場合、「おはよう」と返信
        reply_message = "おはよう。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return

    match = any(pattern.search(user_message) for pattern in hello)
    if match:
        # 一致した場合、「こんにちは。」と返信
        reply_message = "こんにちは。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return

    match = any(pattern.search(user_message) for pattern in good_evening)
    if match:
        # 一致した場合、「こんばんは」と返信
        reply_message = "こんばんは。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return

    match = any(pattern.search(user_message) for pattern in good_night)
    if match:
        # 一致した場合、「おやすみ。」と返信
        reply_message = "おやすみ。。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return
    

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
