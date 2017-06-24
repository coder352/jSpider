# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    info = scrapy.Field()
    desc = scrapy.Field()
class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
class UserItem(scrapy.Item):
    name = scrapy.Field()
    age = scrapy.Field()
    gender = scrapy.Field()
    location = scrapy.Field()
