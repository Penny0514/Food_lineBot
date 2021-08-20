# 這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# 推薦吃什麼


def buttons_message_eat(p):
    city = p[0:3]
    block = p[-3:]
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/NcpwxDg.jpg",
            title="不知道吃什麼？",
            text="選一個唄!",
            actions=[
                MessageTemplateAction(
                    label="抽籤",
                    text="幫我決定!"
                ),
                MessageTemplateAction(
                    label="查看推薦",
                    text="我要看推薦"
                ),
                URITemplateAction(
                    label="去食記逛逛",
                    uri="https://ifoodie.tw/explore/{}/{}/list".format(
                        city, block)
                )
            ]
        )
    )
    return message

# 隨機展示


def buttons_message_random(title, star, add, img, uri):
    message = TemplateSendMessage(
        alt_text='抽籤～',
        template=ButtonsTemplate(
            thumbnail_image_url=img,
            title=title,
            text=star+'顆星' + '  '+add,
            actions=[
                URITemplateAction(
                    label="看食記",
                    uri='https://ifoodie.tw'+uri
                ),
                MessageTemplateAction(
                    label='再抽一次',
                    text='再抽一次'
                ),
                MessageTemplateAction(
                    label='重新選擇',
                    text='重新選擇'
                ),
            ]
        )
    )
    return message

# 旋轉木馬按鈕訊息介面 max=10


def Carousel_Template_advice(title_adv, star_adv, opening_adv, add_adv, img_adv, uri_adv, p_ad):
    message = TemplateSendMessage(
        alt_text='推薦美食',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=img_adv[p_ad[0]],
                    title=title_adv[p_ad[0]],
                    text=star_adv[p_ad[0]]+'顆星'+' '+add_adv[p_ad[0]],
                    actions=[
                        URITemplateAction(
                            label="看食記",
                            uri='https://ifoodie.tw'+uri_adv[p_ad[0]]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_adv[p_ad[1]],
                    title=title_adv[p_ad[1]],
                    text=star_adv[p_ad[1]]+'顆星'+' '+add_adv[p_ad[1]],
                    actions=[
                        URITemplateAction(
                            label="看食記",
                            uri='https://ifoodie.tw'+uri_adv[p_ad[1]]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_adv[p_ad[2]],
                    title=title_adv[p_ad[2]],
                    text=star_adv[p_ad[2]]+'顆星'+' '+add_adv[p_ad[2]],
                    actions=[
                        URITemplateAction(
                            label="看食記",
                            uri='https://ifoodie.tw'+uri_adv[p_ad[2]]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_adv[p_ad[3]],
                    title=title_adv[p_ad[3]],
                    text=star_adv[p_ad[3]]+'顆星'+' '+add_adv[p_ad[3]],
                    actions=[
                        URITemplateAction(
                            label="看食記",
                            uri='https://ifoodie.tw'+uri_adv[p_ad[3]]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_adv[p_ad[4]],
                    title=title_adv[p_ad[4]],
                    text=star_adv[p_ad[4]]+'顆星'+' '+add_adv[p_ad[4]],
                    actions=[
                        URITemplateAction(
                            label="看食記",
                            uri='https://ifoodie.tw'+uri_adv[p_ad[4]]
                        )
                    ]
                ),

            ]
        )
    )
    return message
