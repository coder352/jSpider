# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymongo  # python 中用来操作 mongodb 的库

class JspiderPipeline(object):
    # 初始只有 process_item() 函数
    # 会先调用 from_crawler() 类方法, 然后传递给 __init__() 函数
    # open_spider() -> process_item() -> close_spider()
    # process_item() return item; 会在终端打印, 如果有 -o xx.csv 还会保存到文件
    def __init__(self, use_file, file_name, use_mongo, mongo_uri, mongo_db, mongo_collection):
        # 打开文件
        self.use_file = use_file
        if self.use_file:
            self.file = codecs.open(file_name, 'w', encoding='utf-8')
        # 初始化数据库变量
        self.use_mongo = use_mongo
        if self.use_mongo:  # 这块控制的不是很好, 以后在写
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
        if self.use_mongo:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
        pass
    def close_spider(self, spider):  # 在 spider 工作结束后关闭连接
        if self.use_mongo:
            self.client.close()
        pass
    def process_item(self, item, spider):
        if self.use_file:
            line = json.dumps(dict(item), ensure_ascii=False, indent=2) + '\n'  # item 是一个类对象, 不是 str, 也不是 dict, dumps() 默认接收的是 dict
            self.file.write(line)  # 直接 str(item) 格式不好看
        if self.use_mongo:
            self.db[self.collection_name].insert(dict(item))  # Mongo 可以直接插入 dict, file-like 要写入 str
        return item  # 这里会把结果输送到终端打印出来

