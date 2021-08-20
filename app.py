import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


# ======這裡是呼叫的檔案內容=====
from message import *
from Function import *
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import tempfile
import os
import datetime
from random import randrange
import time
# ======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'v/FEn99f/eDstKZ4HaZ5Jh+mE8DpxQVaz3DSDGgYQpZVdmz6jPO9Xs+cFwOpXKE5NabruFwlGliw4zpJlvsG7Ja4FIdKvW8Jbm5hhw/jBxBPx70aI9tbx8UFRr80pYLUOddiY6BaCqdefAJxohqcyQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f20c4c235b9c5b8c60dc0864a7199887')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(PostbackEvent)
def handle_postback(event):
    quick_reply = event.postback.data
    if 'level' in quick_reply:
        if quick_reply == 'level_1':
            store_priceRange('1')
        elif quick_reply == 'level_2':
            store_priceRange('2')
        elif quick_reply == 'level_3':
            store_priceRange('3')

    else:
        if quick_reply == '小吃':
            store_type('小吃')
        elif quick_reply == '日式':
            store_type('日式料理')
        elif quick_reply == '美式':
            store_type('美式料理')
        elif quick_reply == '韓式':
            store_type('韓式料理')
        elif quick_reply == '甜點':
            store_type('甜點')

        # message = buttons_message_eat()
        line_bot_api.reply_message(
            event.reply_token, buttons_message_eat(get_place()))


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    global titles, stars, adds, images, uri

    # 喚醒後決定區域
    if '等等要吃啥' in msg or '重新選擇' in msg:
        message = TextSendMessage(text='要去哪吃?輸入:縣市+行政區 (ex.台北市信義區)')
        line_bot_api.reply_message(event.reply_token, message)

    # 價位選擇 (quick reply)
    elif '市'in msg or '縣'in msg and '區' in msg:
        store_place(msg)
        # message = buttons_message_eat()
        # message = buttons_message_range()
        # line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='請選擇價位',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                label="150以內", data="level_1", text='150以內')
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label="150~600",  data="level_2", text='150~600')
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label="600~1200", data="level_3", text='600~1200')
                        )
                    ]
                )
            )
        )

    # 種類選擇 (quick reply)
    elif '150以內' in msg or '150~600' in msg or '600~1200' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='想吃什麼類型?',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                label="小吃", data="小吃", text='小吃')
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label="日式料理",  data="日式", text='日式料理')
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label="美式料理",  data="美式", text='美式料理')
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label="韓式料理",  data="韓式", text='韓式料理')
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label="甜點", data="甜點", text='甜點')
                        )
                    ]
                )
            )
        )

    # 看結果
    elif '幫我決定!'in msg:
        titles, stars, adds, images, uri = getFood_random(msg)

        if len(titles) < 1:
            line_bot_api.reply_message(
                event.reply_token,  TextSendMessage(text='此區域和時段無推薦美食'))
        else:
            one = randrange(len(titles))
            message = buttons_message_random(
                titles[one], stars[one], adds[one], images[one], uri[one])
            line_bot_api.reply_message(event.reply_token, message)

    elif '再抽一次' in msg:
        one = randrange(len(titles))
        message = buttons_message_random(
            titles[one], stars[one], adds[one], images[one], uri[one])
        line_bot_api.reply_message(event.reply_token, message)

    elif '我要看推薦' in msg:
        title_ad, stars_ad, opening_ad, adds_ad, images_ad, uri_ad, p_ad = getFood_advice()
        if len(title_ad) < 4:
            content = '這個時間沒有美食可以推薦喔'
            line_bot_api.reply_message(
                event.reply_token,  TextSendMessage(text=content))
        else:
            message = Carousel_Template_advice(
                title_ad, stars_ad, opening_ad, adds_ad, images_ad, uri_ad, p_ad)
            line_bot_api.reply_message(
                event.reply_token, message)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入!輸入"等等要吃啥"讓我幫你做選擇')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
