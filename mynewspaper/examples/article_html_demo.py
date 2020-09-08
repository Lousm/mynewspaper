#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#
# Copyright (c) 2020 LouShimin, Inc. All Rights Reserved
#
# Version : 1.0
# Author  : LouShimin
# Time    : 2020/5/13 08:39
# Desc    :   


import codecs
import requests

from mynewspaper.myarticle import (
    MYArticle
)
from newspaper.article import (
    Article as Origin_Article
)

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

proxies = {
    "http": "http://0.0.0.0:1087",
    "https": "http://0.0.0.0:1087"
}

url = "https://www.dailymail.co.uk/sciencetech/article-6964451/Is-fitness-tracker-LYING-you.html"

html = requests.get(url, headers=headers, proxies=proxies).content

news1 = MYArticle(url, language="en")
news1.set_html(html)
news1.parse()
codecs.open("new_demo.html", mode="w").write(news1.all_article_html)

print("#################### 分割线 ########################")
news2 = Origin_Article(url, language="en")
news2.set_html(html)
news2.parse()
codecs.open("old_demo.html", mode="w").write(news2.article_html)