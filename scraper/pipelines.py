# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymongo
import pymysql
from scraper.items import VesselsItem, MovementItem, PositionItem
from scraper import settings
from scrapy import log

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
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            charset = 'utf8',
            use_unicode = True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        sql = ''
        params = ''

        if isinstance(item, VesselsItem):
            sql = 'insert into expected_vessels(date, ata_eta, vessel, cargo, quantity, ie, agent) values (%s, %s, %s, %s, %s, %s, %s)'
            params = (item['date'], item['ata_eta'], item['vessel'], item['cargo'], item['quantity'], item['ie'], item['agent'])

        elif isinstance(item, MovementItem):
            sql = 'insert into shipping_movement(date, state, vessel_name, berth_allotted, pilot_boarding_time) values (%s, %s, %s, %s, %s)'
            params = (item['date'], item['state'], item['vessel_name'], item['berth_allotted'], item['pilot_boarding_time'])

        elif isinstance(item, PositionItem):
            sql = '''insert into vessel_position(date, berth, vessel, ie, fc, date_of_berthing, cargo, 
            quantity, day_s_handling, up_to_date_hanfling, balance, load_or_discharge_port, agent) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            params = (item['date'], item['berth'], item['vessel'], item['ie'], item['fc'], item['date_of_berthing'], item['cargo'], 
                item['quantity'], item['day_s_handling'], item['up_to_date_hanfling'], item['balance'], item['load_or_discharge_port'], item['agent'])

        try:
            self.cursor.execute(sql, params)
            self.connect.commit()
        except Exception as error:
            log.err(error)

        return item


