# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymongo  # python 中用来操作 mongodb 的库

class JspiderPipeline(object):
    def __init__(self, use_file, file_name, use_mongo, mongo_uri, mongo_db, mongo_collection):
        # 打开文件
        self.use_file = use_file
        if self.use_file:
            self.file = codecs.open(file_name, 'w', encoding='utf-8')
        # 初始化数据库变量
        # if use_mongo:  # 这块控制的不是很好, 以后在写
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = mongo_collection  # mongo 的 collection 相当于 sql 的 table
        self.client, self.db = None, None
    @classmethod
    def from_crawler(cls, crawler):  # 配置 mongo 和 file, 框架会调用 JspiderPipeline.from_crawler()
        return cls(
            use_file = crawler.settings.get('USE_FILE', False),  # 默认不使用文件存储
            file_name = crawler.settings.get('FILE_NAME', 'tmp'),

            use_mongo = crawler.settings.get('USE_MONGO', True),  # 默认使用 MongoDB 存储
            mongo_uri = crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017/'),  # 从 settings 中 mongo 的 uri, 后面是默认值
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'douban'),  # 从 settings 中获取数据库, 默认为 douban
            mongo_collection = crawler.settings.get('MONGO_COLLECTION', 'douban_cartoon')
        )
    def open_spider(self, spider):  # 在 spider 工作开始前连接 mongodb
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_spider(self, spider):  # 在 spider 工作结束后关闭连接
        self.client.close()
    def process_item(self, item, spider):
        if self.use_file:
            line = json.dumps(dict(item), ensure_ascii=False, indent=2) + '\n'  # item 是一个类对象, 不是 str, 也不是 dict, dumps() 默认接收的是 dict
            self.file.write(line)  # 直接 str(item) 格式不好看
        self.db[self.collection_name].insert(dict(item))  # Mongo 可以直接插入 dict, file-like 要写入 str
        return item

