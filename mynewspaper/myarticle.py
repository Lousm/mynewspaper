#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#
# Copyright (c) 2020 LouShimin, Inc. All Rights Reserved
#
# Version : 1.0
# Author  : LouShimin
# Time    : 2020/4/18 15:24
# Desc    :   

import re
import copy
import logging
import hashlib
from lxml import etree

from newspaper.article import (
    Article
)
from newspaper.utils import (
    extend_config
)
from newspaper.text import (
    innerTrim
)
from html import unescape

from newspaper.cleaners import DocumentCleaner
# from newspaper.configuration import Configuration
# from newspaper.extractors import ContentExtractor
# from newspaper.outputformatters import OutputFormatter
from newspaper.utils import (URLHelper, RawHelper, extend_config,
                        get_available_languages, extract_meta_refresh)
from newspaper.videos.extractors import VideoExtractor

from .myextractors import (
    MYContentExtractor
)
from .myconfiguration import (
    MYConfiguration
)
from .outputformatters import (
    MYOutputFormatter
)
from .tools import (
    getMd5,
    get_xpath
)

__title__ = "myarticle"
log = logging.getLogger(__name__)


class ArticleException(Exception):
    pass


class MYArticle(Article):
    def __init__(self, url, title=u'',
                 source_url=u'', config=None, **kwargs):
        self.config = config or MYConfiguration()
        self.config = extend_config(self.config, kwargs)

        self.extractor = MYContentExtractor(self.config)

        self.content_html = ""
        self.not_del_article_html=""

        # add text with tag
        self.text_with_tag = ""

        # add all text
        self.all_text = ""

        # html content
        self.all_article_html = ""

        # all imgs
        self.all_imgs = []

        super(MYArticle, self).__init__(
            url, title=title, source_url=source_url, config=config, **kwargs
        )

    def set_text_with_tag(self, nodes):
        """
        新增一个text with tag
        :param node:
        :return:
        """
        if not nodes:
            return

        content = []
        for node in nodes:
            try:
                content.append(etree.tostring(node, method="html").decode())
            except Exception as msg:
                print(msg)

        self.text_with_tag = "<br>".join(content)

    def set_all_text(self, output_formatter, nodes):
        """
        根据得到的 top node的attrib 信息获取其他的div内容
            Demo URL：

        :param node:
        :return:
        """
        if not nodes:
            return

        content = []
        for node in nodes:
            try:
                # text,html = output_formatter.get_formatted(node)
                # content.append(text)
                # self.all_article_html += html
                # txt = etree.tostring(node)
                txts = [i for i in node.itertext()]
                txt = innerTrim(' '.join(txts).strip())

                if txt:
                    txt = unescape(txt)
                    txt_lis = innerTrim(txt).split(r'\n')
                    txt_lis = [n.strip(' ') for n in txt_lis]
                    content.extend(txt_lis)

                self.all_article_html += etree.tostring(node, method='html').decode()

                # cnt = re.sub("<.*?>", "", html).strip()
                # content.append(cnt)

                pass
            except Exception as message:
                print(message)

        self.all_text = '\n\n'.join(content)

    def set_not_del_all_text(self, output_formatter, nodes):
        """
        根据得到的 top node的attrib 信息获取其他的div内容
            Demo URL：

        :param node:
        :return:
        """
        if not nodes:
            return

        content = []
        for node in nodes:
            try:
                # text,html = output_formatter.get_formatted(node)
                # content.append(text)
                # self.all_article_html += html
                # txt = etree.tostring(node)
                txts = [i for i in node.itertext()]
                txt = innerTrim(' '.join(txts).strip())

                if txt:
                    txt = unescape(txt)
                    txt_lis = innerTrim(txt).split(r'\n')
                    txt_lis = [n.strip(' ') for n in txt_lis]
                    content.extend(txt_lis)

                self.not_del_article_html += etree.tostring(node, method='html').decode()

                # cnt = re.sub("<.*?>", "", html).strip()
                # content.append(cnt)

                pass
            except Exception as message:
                print(message)



    def get_all_valid_node(self, doc, node):
        """
        获取所有可用节点
        :param node:
        :return:
        """
        values = dict(node.attrib)

        xpath = []
        remove_attr = ["gravityScore", "gravityNodes"]
        for attr in remove_attr:
            if attr in values:
                del values[attr]

        if not values:
            return [node]

        for k,v in values.items():
            tmp = "@{}=\'{}\'".format(
                k,v
            )
            xpath.append(tmp)

        attrs = ' and '.join(xpath)
        xpath_rule = ".//{}[{}]".format(
            node.tag,
            attrs
        )

        nodes = doc.xpath(xpath_rule)


        return self.filter_invalid_nodes(nodes)

    def get_not_del_all_valid_node(self,top_node,not_deldom):
        """
        获取所有可用节点
        :param node:
        :return:
        """
        xpath_list=[]
        not_clean_html=""
        top_xpath=""
        xpath_end = top_node.tag
        xpath_attrib = top_node.attrib.get("class")
        if xpath_attrib is not None:
            top_xpath = get_xpath(top_node, xpath_end + "[@class='" + xpath_attrib + "']")
        elif top_node.attrib.get("id") is not None:
            top_xpath = get_xpath(top_node, xpath_end + "[@id='" + top_node.attrib.get("id") + "']")
        else:
            top_xpath = get_xpath(top_node, xpath_end)

        best_node_list=not_deldom.xpath("//"+top_xpath)
        if len(best_node_list)==0:
            return ""
        best_node_list = self.get_top_image(best_node_list)
        best_node_list=self.not_del_filter_invalid_nodes(best_node_list)
        del_nodes=[]
        after_str=""
        for simple in best_node_list:
            html_str=etree.tostring(simple, method="html").decode()
            if html_str in after_str:
                del_nodes.append(simple)
            else:
                after_str=after_str+html_str
        for del_node in del_nodes:
            best_node_list.remove(del_node)
        for simple_node in best_node_list:
            not_clean_html = not_clean_html +etree.tostring(simple_node, method="html").decode()

            # not_clean_html = etree.tostring(not_clean_dom, method="html").decode()

        return not_clean_html


    def filter_invalid_nodes(self, nodes, rewrite_links_tag=True):
        """
            TODO:
                1、过滤标签的的说明文字，同时保存图片
                2、做法，就是找到图片节点往上提
                3、图片提取有问题，这部分后续需要重新做规划
                    Badcase wiki:
                        https://www.usatoday.com/story/sports/high-school/2020/05/29/basketball-recruiting-kennedy-chandler-transfer-sunrise-christian-briarcrest/5280012002/

        """
        parser = self.config.get_parser()
        new_nodes = []
        for node in nodes:
            # del video tag 及其子节点
            invalid_nodes = node.xpath(".//*[contains(@class, 'Video') or contains(@class, 'video') or contains(@id, 'page') or contains(@class, 'share') or contains(@class, 'follow-google') or contains(@class, 'cookies-warning') or contains(@class, 'Image_caption')]")
            for vn in invalid_nodes:
                for d in vn.getchildren():
                    vn.remove(d)

            # clear tag
            if rewrite_links_tag:
                node = parser.clean_article_html(node)

            figures = node.xpath(".//figure | .//figcaption")
            if figures:
                for figure in figures:
                    imgs = figure.xpath(".//img | .//image")

                    # 删除文字说明
                    # for f in figure.getchildren():
                    #     figure.remove(f)

                    i = 0
                    for img in imgs:
                        md_value = ""
                        # img src
                        attrib = dict(img.attrib)
                        src=attrib.get('data-src')
                        if src ==None:
                            src=attrib.get('src')
                        # src = (attrib.get('src') or
                        #        attrib.get('data-src')
                        # )
                        if src:
                            self.all_imgs.append(src)
                            md_value = getMd5(src)

                            # clear
                            img.attrib.clear()
                            img.attrib["src"] = src
                        else:
                            # 如果没有src 这部分图片标签需要去除
                            img.getparent().remove(img)
                            continue

                        # add attrib
                        img.attrib["md5"] = md_value
                        figure.insert(i, img)
                        i += 0
            else:
                imgs = node.xpath(".//img | .//image")
                for img in imgs:
                    md_value = ""
                    # img src
                    attrib = dict(img.attrib)
                    src = attrib.get('data-src')
                    if src == None:
                        src = attrib.get('src')
                    # src = (attrib.get('src') or
                    #        attrib.get('data-src')
                    #        )
                    if src:
                        self.all_imgs.append(src)
                        md_value = getMd5(src)

                        # 清空
                        img.attrib.clear()
                        img.attrib["src"] = src
                    else:
                        # 如果没有src 这部分图片标签需要去除
                        img.getparent().remove(img)
                        continue

                    # add attrib
                    img.attrib["md5"] = md_value
            new_nodes.append(node)
        return new_nodes




    def not_del_filter_invalid_nodes(self, nodes, rewrite_links_tag=True):
        """
            TODO:
                1、过滤标签的的说明文字，同时保存图片
                2、做法，就是找到图片节点往上提
                3、图片提取有问题，这部分后续需要重新做规划
                    Badcase wiki:
                        https://www.usatoday.com/story/sports/high-school/2020/05/29/basketball-recruiting-kennedy-chandler-transfer-sunrise-christian-briarcrest/5280012002/

        """
        parser = self.config.get_parser()
        new_nodes = []
        for node in nodes:
            # del video tag 及其子节点
            invalid_nodes = node.xpath(".//*[contains(@class, 'Video') or contains(@class, 'video') or contains(@id, 'page') or contains(@class, 'share') or contains(@class, 'follow-google') or contains(@class, 'cookies-warning') or contains(@class, 'Image_caption')]")
            for vn in invalid_nodes:
                for d in vn.getchildren():
                    vn.remove(d)
            imgs = node.xpath(".//img | .//image")
            for img in imgs:
                md_value = ""
                # img src
                attrib = dict(img.attrib)
                src = attrib.get('data-src')
                if src == None:
                    src=attrib.get('data-lazy-src')
                if src == None:
                    src = attrib.get('src')
                # src = (attrib.get('src') or
                #        attrib.get('data-src')
                #        )
                if src:
                    self.all_imgs.append(src)
                    md_value = getMd5(src)

                    # 清空
                    img.attrib.clear()
                    img.attrib["src"] = src
                else:
                    # 如果没有src 这部分图片标签需要去除
                    img.getparent().remove(img)
                    continue

                # add attrib
                img.attrib["md5"] = md_value
            new_nodes.append(node)
        return new_nodes

    def get_top_image(self,node):
        parent_dom = node[0].getparent()
        i=0
        img_node=None
        try:
            if parent_dom.getchildren().index(node[0])==0:
                while True:
                    if len(parent_dom.getparent().getchildren())==1:
                        parent_dom=parent_dom.getparent()
                        continue
                    dom_index=parent_dom.getparent().getchildren().index(parent_dom)
                    if dom_index==0:
                        parent_dom = parent_dom.getparent()
                        continue
                    else:
                        break
            else:

                dom_index=parent_dom.getchildren().index(node[0])
                parent_dom = node[0]
        except:
            return node
        while i<2:
            try:
                if dom_index - i ==0:
                    break
                up_dom = parent_dom.getparent().getchildren()[dom_index - i - 1]
                # if up_dom.tag=="p" and up_dom.text=="":
                #     continue
                up_dom_text = up_dom.xpath(".//img")
                if len(up_dom_text) !=0:
                    img_node=up_dom_text[0].getparent()
                    # print(up_dom_text[0].attrib["src"])
                    break
                i=i+1
            except Exception as e:
                img_node=None
                break
        if img_node is None:
            return node
        else:
            node.insert(0, img_node)
            return node






    def parse(self):
        self.throw_if_not_downloaded_verbose()
        re_comment = re.compile('<!--[^>]*-->')
        self.html = re_comment.sub('', self.html)
        self.doc = self.config.get_parser().fromstring(self.html)
        self.not_del_doc=self.doc
        self.doc.make_links_absolute(self.url)
        self.clean_doc = copy.deepcopy(self.doc)

        if self.doc is None:
            # `parse` call failed, return nothing
            return

        # TODO: Fix this, sync in our fix_url() method
        parse_candidate = self.get_parse_candidate()
        self.link_hash = parse_candidate.link_hash  # MD5

        output_formatter = MYOutputFormatter(self.config)
        document_cleaner = DocumentCleaner(self.config)
        # output_formatter = OutputFormatter(self.config)

        title = self.extractor.get_title(self.clean_doc)
        self.set_title(title)

        authors = self.extractor.get_authors(self.clean_doc)
        self.set_authors(authors)

        meta_lang = self.extractor.get_meta_lang(self.clean_doc)
        self.set_meta_language(meta_lang)

        if self.config.use_meta_language:
            self.extractor.update_language(self.meta_lang)
            output_formatter.update_language(self.meta_lang)

        meta_favicon = self.extractor.get_favicon(self.clean_doc)
        self.set_meta_favicon(meta_favicon)

        meta_description = \
            self.extractor.get_meta_description(self.clean_doc)
        self.set_meta_description(meta_description)

        canonical_link = self.extractor.get_canonical_link(
            self.url, self.clean_doc)
        self.set_canonical_link(canonical_link)

        tags = self.extractor.extract_tags(self.clean_doc)
        self.set_tags(tags)

        meta_keywords = self.extractor.get_meta_keywords(
            self.clean_doc)
        self.set_meta_keywords(meta_keywords)

        meta_data = self.extractor.get_meta_data(self.clean_doc)
        self.set_meta_data(meta_data)

        self.publish_date = self.extractor.get_publishing_date(
            self.url,
            self.clean_doc)




        # Before any computations on the body, clean DOM object
        not_deldom=copy.deepcopy(self.doc)
        self.doc = document_cleaner.clean(self.doc)
        # str1=etree.tostring(self.doc,method="html")
        self.top_node = self.extractor.calculate_best_node(self.doc)
        if self.top_node is not None:
            # get 所有相似 Node
            valid_nodes = self.get_all_valid_node(self.doc, self.top_node)
            # 获取原始页面的最优节点
            # not_del_html=self.get_not_del_xpath(valid_nodes,self.not_del_doc,check_str_list)
            not_del_html=self.get_not_del_all_valid_node(self.top_node,not_deldom)
            if not_del_html!="":
                self.not_del_article_html=not_del_html
            # add text with tag
            self.set_text_with_tag(valid_nodes)

            # get all text
            self.set_all_text(output_formatter, valid_nodes)

            video_extractor = VideoExtractor(self.config, self.top_node)
            self.set_movies(video_extractor.get_videos())

            self.top_node = self.extractor.post_cleanup(self.top_node)
            self.clean_top_node = copy.deepcopy(self.top_node)

            text, article_html = output_formatter.get_formatted(
                self.top_node)
            self.set_article_html(article_html)
            self.set_text(text)
            if not_del_html=="":
                self.not_del_article_html=self.all_article_html

        self.fetch_images()

        self.is_parsed = True
        self.release_resources()
