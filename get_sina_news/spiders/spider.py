# -*- coding: utf-8 -*-
import scrapy
from get_sina_news.items import SinaNewsItem


class SinaNewsSpider(scrapy.Spider):
    name = 'sina_news'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 　以一级目录的“新闻”作为根来循环遍历所有的一级目录
        for each in response.xpath("//div[@id='tab01']/div[@data-sudaclick!='newsnav']"):
            # 获取一级目录的url
            first_url = each.xpath('./h3/a/@href').extract_first()
            #　循环遍历二级目录url
            for other in each.xpath("./ul/li/a"):
                #　获取二级目录的url
                if other.xpath('./@href').extract_first().startswith(first_url):
                    item = SinaNewsItem()
                    second_url = other.xpath('./@href').extract_first()
                    item['first_url'] = first_url
                    item['second_url'] = second_url
                    # 获取二级目录请求
                    yield scrapy.Request(url=item['second_url'],meta={'meta1':item},callback=self.second_catalog_parse)

    def second_catalog_parse(self,response):
        meta_1 = response.meta['meta1']
        items = []
        # 循环遍历获取文章url
        for each in response.xpath('//a/@href'):
            if each.extract().encode('utf-8').startswith(meta_1['first_url'].encode('utf-8')) and each.extract().encode('utf-8').endswith('.shtml'.encode('utf-8')):
                item = SinaNewsItem()
                item['first_url'] = meta_1['first_url']
                item['second_url'] = meta_1['second_url']
                item['article_url'] = each.extract()
                items.append(item)
                # 获取文章请求
                for each in items:
                    yield scrapy.Request(each['article_url'],meta={'meta2':each},callback=self.article_parse)

    def article_parse(self,response):
        item = response.meta['meta2']
        # 获取文章的标题，时间，文章内容
        item['head'] = ''.join(response.css("h1::text").extract())
        item['time'] = ''.join(response.xpath("//div[@id='top_bar']/div/div[2]/span/text()").extract())
        item['article'] = ''.join(response.xpath("//div[@id='artibody']/p/text()").extract())
        # 由于item里面还包含了一级目录和二级目录的url我将它们剔除
        item1 = {
            'head':item['head'],
            'time':item['time'],
            'article':item['article']
        }
        if '2018年11月15日' in str(item1['time']):
            yield item1


