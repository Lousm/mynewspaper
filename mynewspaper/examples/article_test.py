#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#
# Copyright (c) 2020 LouShimin, Inc. All Rights Reserved
#
# Version : 1.0
# Author  : LouShimin
# Time    : 2020/4/18 15:35
# Desc    :   

import requests

from mynewspaper import (
    Article
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

url = "https://uk.investing.com/currencies/eur-gbp"

html = requests.get(url, headers=headers).content
news = Article(url, language="en")
news.set_html(html)
news.parse()
print(news.title)
print(news.text)


