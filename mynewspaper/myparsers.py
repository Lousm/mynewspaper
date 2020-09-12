#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2020 LouShimin, Inc. All Rights Reserved
#
# Version : 1.0
# Author  : LouShimin
# Time    : 2020/4/18 15:03
# Desc    :   

import lxml.html

from newspaper.parsers import (
    Parser
)


class MYParse(Parser):

    @classmethod
    def clean_article_html(cls, node):
        """
        删除原来标签中的 <a href=""> </a>
        :param node:
        :return:
        """
        article_cleaner = lxml.html.clean.Cleaner()
        article_cleaner.javascript = True
        article_cleaner.style = True
        article_cleaner.allow_tags = [
            'span', 'p', 'br', 'strong', 'b', 'td',
            'em', 'i', 'tt', 'code', 'pre', 'blockquote', 'img',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'dl', 'dt', 'dd',
            'a', 'figure', 'figcaption', 'image', 'table',
            'picture'
        ]
        article_cleaner.remove_unknown_tags = False
        article_cleaner.safe_attrs = ['src']
        return article_cleaner.clean_html(node)

    pass
