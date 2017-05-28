# -*- coding: utf-8 -*-
import scrapy
from ..items import ImageItem

class ImageSpider(scrapy.Spider):
    name = "image"
    allowed_domains = ["douban.com"]
    start_urls = [
        'https://book.douban.com/tag/哲学',
    ]

    def parse(self, response):
        item = ImageItem()
        # //*[@id="subject_list"]/ul/li[1]/div[1]/a/img
        item['image_urls'] = response.xpath('//*[@id="subject_list"]/ul/li/div[1]/a/img/@src').extract()  # 会爬去整个页面上所有书籍图片
        # //*[@id="subject_list"]/ul/li[1]/div[2]/h2/a
        item['images'] =  response.xpath('//*[@id="subject_list"]/ul/li/div[2]/h2/a/@title').extract()
        return item

# 下载图片其实 pipeline.py 的额外工作而已, 大致分为以下几步:
# 在 Spider 中, 额外定义一个 image_urls 用来存放图片链接的 item
# 这个 item 会从 spider 中传递到 pipeline 中
# 在这个 item 到了 ImagesPipeline 后, 里面的 url 经由 scheduler 插队到 downloader 进行下载
# 下载完成后, Scrapy 会新建一个 files 字段用于存放结果
# 需要额外安装 PIL 保证正常工作

# 步骤:
# 1. 在 settings.py 的 ITEM_PIPELINES 中加入
# 'scrapy.pipelines.images.ImagesPipeline':1,
# 2. 在 settings.py 中添加图片存放目录,如
# IMAGES_STORE = '/home/coder352/Documents/thiscandel/images'
# IMAGES_URLS_FIELD = 'image_urls'
# IMAGES_RESULT_FIELD = 'images'
# 3. 在 items.py 中建立相应的 item
# class ImageItem(scrapy.Item):
#     image_urls = scrapy.Field()
#     images = scrapy.Field()
