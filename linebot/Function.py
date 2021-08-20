# 這個檔案的作用是：建立功能列表

# ===============這些是LINE提供的功能套組，先用import叫出來=============
import requests
from random import *
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from message import *
# ===============LINEAPI=============================================


def getFood_advice():
    eat_place = get_place()
    limit = get_priceRange()
    food = get_type()
    city = eat_place[0:3]
    block = eat_place[-3:]
    titles = []
    stars = []
    openings = []
    adds = []
    images = []
    uri = []

    url = 'https://ifoodie.tw/explore/{}/{}/list/{}?priceLevel={}&sortby=rating'.format(
        city, block, food, limit)

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    # 爬取前10筆餐廳卡片資料
    cards = soup.find_all(
        'div', {'class': 'jsx-3440511973 restaurant-info'})

    if len(cards) == 0:
        content = '此區域和時段無推薦美食'
    else:
        p = sample(range(len(cards)), len(cards))
    for card in cards:
        # 餐廳名稱
        title = card.find(
            "a", {"class": "jsx-3440511973 title-text"}).getText()
        titles.append(title)

        # 餐廳評價
        if card.find("div", {"class": "jsx-1207467136 text"}):
            stars.append(card.find(
                "div", {"class": "jsx-1207467136 text"}).getText())
        else:
            stars.append('無評價')
        # 餐廳評價
        openings.append(card.find(
            "div", {"class": "jsx-3440511973 info"}).getText())
        # 餐廳地址
        adds.append(card.find(
            "div", {"class": "jsx-3440511973 address-row"}).getText())
        # 餐廳照片
        if card.find('img', {"alt": title}).get("data-src"):
            images.append(
                card.find('img', {"alt": title}).get("data-src"))
        else:
            images.append(
                card.find('img', {"alt": title}).get("src"))
        # 食記網址
        uri.append(
            card.find("a", {"class": "jsx-3440511973"}).get("href"))

    return titles, stars, openings, adds, images, uri, p


def getFood_random(msg):
    eat_place = get_place()
    limit = get_priceRange()
    food = get_type()
    city = eat_place[0:3]
    block = eat_place[-3:]

    if msg == '再抽一次':
        one = randrange(len(titles))
        return titles[one], stars[one], adds[one], images[one], uri[one]
    else:
        titles = []
        stars = []
        adds = []
        images = []
        uri = []
        for page in range(2):
            url = 'https://ifoodie.tw/explore/{}/{}/list/{}?priceLevel={}&opening=true&sortby=popular&page={}'.format(
                city, block, food, limit, page+1)

            response = requests.get(url)

            soup = BeautifulSoup(response.content, "html.parser")

            # 爬取前2頁餐廳卡片資料
            cards = soup.find_all(
                'div', {'class': 'jsx-3440511973 restaurant-info'})
            for card in cards:
                if card.find("a", {"class": "jsx-3440511973 ad-info-link"}):
                    continue
                else:
                    # 餐廳名稱
                    title = card.find(
                        "a", {"class": "jsx-3440511973 title-text"}).getText()
                    titles.append(title)
                    # 餐廳評價
                    if card.find("div", {"class": "jsx-1207467136 text"}):
                        stars.append(card.find(
                            "div", {"class": "jsx-1207467136 text"}).getText())
                    else:
                        stars.append('無評價')
                    # 餐廳地址
                    adds.append(card.find(
                        "div", {"class": "jsx-3440511973 address-row"}).getText())
                    # 餐廳照片
                    if card.find('img', {"alt": title}).get("data-src"):
                        images.append(
                            card.find('img', {"alt": title}).get("data-src"))
                    else:
                        images.append(
                            card.find('img', {"alt": title}).get("src"))
                    # 食記網址
                    uri.append(
                        card.find("a", {"class": "jsx-3440511973"}).get("href"))

        return titles, stars, adds, images, uri


def store_place(p):
    global place
    place = p


def get_place():
    return place


def store_priceRange(msg):
    global price
    price = msg


def get_priceRange():
    return price


def store_type(food):
    global type_eat
    type_eat = food


def get_type():
    return type_eat
