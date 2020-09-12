#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2020 LouShimin, Inc. All Rights Reserved
#
# Version : 1.0
# Author  : LouShimin
# Time    : 2020/5/13 15:31
# Desc    :   

import hashlib
from lxml import etree


def getMd5(str):
    m2 = hashlib.md5()
    m2.update(str.encode('utf-8'))
    return m2.hexdigest()


def get_xpath(dom, xpath):
    # print(dom.tag)
    parent_dom = dom.getparent()
    attrib_name = ""
    if parent_dom.tag == "body" or parent_dom.tag == "html":
        return xpath
    else:

        try:
            attrib_name = parent_dom.attrib["class"]
            if attrib_name == "":
                dom_xpath = parent_dom.tag
            else:
                dom_xpath = parent_dom.tag + "[@class='" + attrib_name + "']"
        except Exception as e:
            try:
                attrib_name = parent_dom.attrib["id"]
                if attrib_name == "":
                    dom_xpath = parent_dom.tag
                else:
                    dom_xpath = parent_dom.tag + "[@id='" + attrib_name + "']"
            except Exception as e:
                dom_xpath = parent_dom.tag
        if attrib_name == "":
            children_list = parent_dom.getparent().xpath(dom_xpath)
            xpath_index = children_list.index(parent_dom) + 1
            dom_xpath = dom_xpath

        xpath = dom_xpath + "/" + xpath

        return get_xpath(parent_dom, xpath)
