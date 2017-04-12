# -*- coding:utf-8 -*-
import scrapy
from selenium import webdriver
import selenium
from scrapy import Request
from scrapy.http import HtmlResponse
import time
import json

js = """
function scrollToBottom() {

    var Height = document.body.clientHeight,  //文本高度
        screenHeight = window.innerHeight,  //屏幕高度
        INTERVAL = 100,  // 滚动动作之间的间隔时间
        delta = 500,  //每次滚动距离
        curScrollTop = 0;    //当前window.scrollTop 值

    var scroll = function () {
        curScrollTop = document.body.scrollTop;
        window.scrollTo(0,curScrollTop + delta);
    };

    var timer = setInterval(function () {
        var curHeight = curScrollTop + screenHeight;
        if (curHeight >= Height){   //滚动到页面底部时，结束滚动
            clearInterval(timer);
        }
        scroll();
    }, INTERVAL)
}
scrollToBottom()
"""
class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        #request = Request(url= 'http://www.leiphone.com/', dont_filter=True)
        #request.meta['PhantomJS'] = True
        #if request.meta.has_key('PhantomJS'):
        if spider.name == 'test2':
            driver = webdriver.PhantomJS()
            driver.get(request.url)
            for i in range(3):
                driver.execute_script(js)
                time.sleep(5)
            print 'OK......................'
            content = driver.page_source.encode('utf-8')
            driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)