# -*- coding: utf-8 -*-
import scrapy
import re
import random
from scrapy import Request
from proxypool.proxypool import *

class HaitouSpider(scrapy.Spider):
    name = 'haitou'
    allowed_domains = ['haitou.cc']
    start_urls = ['https://xjh.haitou.cc/']

    def parse(self, response):
        pool_list = get_pool('1')
        for index in range(1,190):
            url = 'https://xjh.haitou.cc/wh/page-' + str(index)
            ran = random.randint(0, pool_list.__len__()-1)
            proxy = 'http://' + pool_list[ran]
            print(proxy)
            yield Request(url, callback=self.parse_data, meta={"proxy": proxy})


    def parse_data(self, response):
        trs = response.xpath('//tr[@data-source="xjh"]').extract()
        pattern = re.compile(
            r'(?s).*?class="cxxt-title".*?<a href="(.*?)" title="(.*?)\n(.*?)\n(.*?)".*?hold-ymd">(.*?)</span>')

        for tr in trs:
            res = re.findall(pattern, tr)
            for r in res:
                url = r[0]
                if url.startswith('/article'):
                    url = 'https://xjh.haitou.cc' + url
                firm = r[1]
                campus = r[2].replace('学校：', '')
                place = r[3].replace('地点：', '')
                time = r[4]

                item = {}
                item['url'] = url
                item['firm'] = firm
                item['campus'] = campus
                item['place'] = place
                item['time'] = time
                yield(item)


