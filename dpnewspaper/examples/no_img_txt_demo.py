#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from dpnewspaper import Article
import requests


headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': '*/*',
    'dnt': '1',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
}

url = "https://www.espn.in/football/uefa-champions-league/story/4088122/arsenal-can-forget-champions-leaguepsg-presidents-tv-negotiationschelseas-kepa-conundrum"

html = requests.get(url, headers=headers).content

news = Article(url, language="en")
news.set_html(html)
news.parse()
tt = "titlse"

print(news.title)
# print(news.images)
print(news.top_img)
print(news.text)
