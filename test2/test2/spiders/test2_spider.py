# -*- coding:utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from test2.items import Test2Item
from scrapy import Request
from scrapy.utils.response import get_base_url
import re

class Test2Spider(Spider):
    name = 'test2'
    start_urls = [
        'http://www.leiphone.com/'
    ]

    def parse(self, response):
        #sel = Selector(response)
        #item = Test1Item()
        #item['link'] = sel.xpath('//h3/a/@href').extract()
        #item['title'] = sel.xpath('//h3/a/@title').extract()
        #yield item
        #print "-----------------"
        items = []
        sel = Selector(response)
        #base_url = get_base_url(response)
        postTitle = sel.css('div.box div.word')
        postTime = sel.css('div.box div.word div.time')
        postAuthor = sel.css('div.box div.word div.msg')
        #print base_url
        #print "=============length======="
        #postCon = sel.css('div.postCon div.c_b_p_desc')
	    #标题、url和描述的结构是一个松散的结构，后期可以改进
        for index in range(len(postTitle)):
            item = Test2Item()
            c = postTitle[index].css('h3').xpath('a/text()').extract()[0]
            d = re.sub(r'\s+', '', c)
            item['title'] = d
            #print item['title'] + "***************\r\n"
            item['link'] = postTitle[index].css('h3').xpath('a/@href').extract()[0]
            item['updated'] = postTime[index].xpath('text()').extract()[0]
            a = postAuthor[index].xpath('a/text()').extract()[1]
            b = re.sub(r'\s+', '', a)
            item['author'] = b
            #item['listUrl'] = base_url
            #item['desc'] = postCon[index].xpath('text()').extract()[0]
	        #print base_url + "********\n"
            items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'
        return items