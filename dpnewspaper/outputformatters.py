#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#
# Copyright (c) 2020 daypop.ai, Inc. All Rights Reserved
#
# Version : 1.0
# Author  : luoyingbo@daypop.ai
# Time    : 2020/4/24 00:03
# Desc    :

__title__ = 'newspaper'

import logging
import simplejson as json

from html import unescape

from newspaper.text import innerTrim
from newspaper.outputformatters import (
    OutputFormatter
)

log = logging.getLogger(__name__)


class DPOutputFormatter(OutputFormatter):

    def __init__(self, config):
        super(DPOutputFormatter, self).__init__(config)

    def convert_to_text(self):
        """
            删除图片说明目前两种策略:
                1、node.attrib 不为空，但class中存在 img/image 等等变量，则为图片文字
                2、node.attrib 不为空，但是只有一个的node节点有此，则也为图片文字说明
        :return:
        """
        has_img_attrib,has_attrib,filter_special_tag = [],[],[]

        for node in list(self.get_top_node()):
            try:
                attrib = ''.join(node.attrib.values()).lower()
            except ValueError as err:  # lxml error
                log.info('%s ignoring lxml node error: %s', __title__, err)
                continue

            try:
                if ('img' in attrib or
                        'image' in attrib or
                        'pic' in attrib or
                        'photo' in attrib or
                        'caption' in attrib
                ):
                    has_img_attrib.append(node)
                elif 'figure' in node.tag.lower():  # 过滤些特殊的标签
                    filter_special_tag.append(node)
                elif 'figcaption' in node.tag.lower():  # 过滤些特殊的标签
                    filter_special_tag.append(node)
                elif node.attrib:       # node.attrib == {}
                    has_attrib.append(node)
            except Exception as err:
                log.info('%s ignoring lxml node error: %s', __title__, err)
                continue

        txts = []
        for node in list(self.get_top_node()):
            if node in has_img_attrib:  # 图片属性
                continue

            if node in filter_special_tag:
                continue

            if (len(has_attrib) == 1 and    # 只有一张图片
                    node in has_attrib):
                continue

            try:
                txt = self.parser.getText(node)
            except ValueError as err:  # lxml error
                log.info('%s ignoring lxml node error: %s', __title__, err)
                txt = None

            if txt:
                txt = unescape(txt)
                txt_lis = innerTrim(txt).split(r'\n')
                txt_lis = [n.strip(' ') for n in txt_lis]
                txts.extend(txt_lis)
        return '\n\n'.join(txts)
