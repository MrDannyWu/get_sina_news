# -*- coding: utf-8 -*-

import scrapy


class SinaNewsItem(scrapy.Item):
    # 一级目录url
    first_url = scrapy.Field()
    # 二级目录url
    second_url = scrapy.Field()
    # 文章url
    article_url = scrapy.Field()
    # 文章标题
    head = scrapy.Field()
    # 文章内容
    article = scrapy.Field()
    # 文章时间
    time = scrapy.Field()
