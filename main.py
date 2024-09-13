from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import re
import os
import dotenv
import requests

app = Flask(__name__)

# LINEのチャネル設定
dotenv.load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
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
    re.compile(r'hey 地原', re.IGNORECASE)  # "hey 地原"用の正規表現
]

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

# メッセージイベントの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 正規表現で部分一致をチェック
    if any(pattern.search(user_message) for pattern in keywords[:-1]):
        # 一致した場合、「地原な。」と返信
        reply_message = "地原な。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    elif re.match(r'hey 地原、今日の献立', user_message, re.IGNORECASE):
        # 献立を提案する
        menu = get_menu()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=menu)
        )

def get_menu():
    # RecipePuppy APIのURL
    url = "http://www.recipepuppy.com/api/"
    params = {
        'q': 'dinner',  # 料理のカテゴリ
        'p': 1  # ページ番号
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        # 例: 最初の3つのレシピタイトルを取得
        recipes = data['results'][:3]
        menu_items = [f"{i+1}. {recipe['title']}" for i, recipe in enumerate(recipes)]
        return "今日の献立:\n" + "\n".join(menu_items)
    else:
        return "今日の献立は準備できませんでした。"

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
