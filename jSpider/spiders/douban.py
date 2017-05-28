# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]  # 爬取不会超出这个范围
    start_urls = (
        'https://book.douban.com/tag/%E6%BC%AB%E7%94%BB?start=0&type=T',  # 豆瓣图书标签: 漫画
    )  # 指定开始的 URL

    def parse(self, response):  # 抓取整个页面后完毕后默认执行的代码
        item = DoubanItem()
        for sel in response.css('#subject_list > ul > li > div.info'):
            item['title'] = sel.css('h2 > a::text').extract_first()
            item['link'] = sel.css('h2 > a::attr(href)').extract_first()
            item['info'] = sel.css('div.pub::text').extract_first()
            item['desc'] = sel.css('p::text').extract_first()
            yield item  # 将 item 传出到 pipelines.py 中...
        # 自动翻页..., 会一直爬下去
        href = response.xpath('//*[@id="subject_list"]/div[2]/span[4]/a')  # F12 找到底部的 "下一页标记", Copy Xpath
        url = u'https://book.douban.com'+ href.css('a::attr(href)').extract_first()
        yield Request(url, callback=self.parse)
