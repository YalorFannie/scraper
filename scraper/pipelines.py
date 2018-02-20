# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymongo
from scraper.items import VesselsItem, MovementItem, PositionItem

class ScraperPipeline(object):
	def __init__(self):
		self.file = codecs.open('expected_vessels.txt', 'w', encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False) + "\n"
		self.file.write(line)
		return item

	def spider_closed(self, spider):
		self.file.close()

class MongoPipeline(object):

    # collection_name = 'expected_vessels'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGODB_DBNAME', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = 'expected_vessels'

        if isinstance(item, VesselsItem):
            collection_name = 'expected_vessels'

        elif isinstance(item, MovementItem):
            collection_name = 'shipping_movement'

        elif isinstance(item, PositionItem):
            collection_name = 'vessel_position'


        self.db[collection_name].insert_one(dict(item))

        return item

class MySqlPipeline(object):
    pass






