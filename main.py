from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random, re, os, dotenv

app = Flask(__name__)

# LINEのチャネル設定
dotenv.load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# パターンと返信メッセージの辞書
patterns = {
    "funny": ([
        r'おもろ', r'おもしろ', r'面白い', r'うける', r'笑った', r'わらった', 
        r'涙出る', r'涙出た', r'最高', r'さいこう', r'さいこー', r'天才', r'神'
    ], "ありがとう。"),
    "keywords": ([
        r'千原', r'ちはら', r'ちーちゃん', r'ちはらっち', r'茅原', r'苑原', 
        r'chihara', r'tihara', r'チハラ', r'田原', r'地腹', r'血はら', 
        r'ちんこ', r'ちんちん', r'チンチン'
    ], "地原な。"),
    "thanks": ([r'さんきゅ', r'サンキュ', r'thank', r'ありがと'], "どういたしまして。"),
    "sorry": ([r'ごめん', r'遅れる', r'遅くなる', r'遅刻'], random.choice(["許さん。", "いいよ。"])),
    "hey": ([r'やっほ', r'ヤッホ'], "やっほー。"),
    "good_morning": ([r'おはよ'], "おはよう。"),
    "hello": ([r'こんにち', r'こんちは', r'こんちわ'], "こんにちは。"),
    "good_evening": ([r'こんばん'], "こんばんは。"),
    "good_night": ([r'おやす', r'寝る', r'ねる', r'ねむい', r'眠い'], "おやすみ。"),
    "are_you_ok": ([r'大丈夫？'], "大丈夫。"),
    "lonely": ([r'寂しい', r'さみしい'], "どうしたの。"),
    "not_lonely": ([r'寂しくない', r'さみしくない'], "寂しくない。"),
    "something_happen": ([r'どうした', r'なんかあった', r'何かあった'], "なんでもない。")
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
    return None

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
