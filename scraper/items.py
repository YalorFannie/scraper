# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VesselsItem(scrapy.Item):
	today = scrapy.Field()
	date = scrapy.Field()
	ata_eta = scrapy.Field()
	vessel = scrapy.Field()
	cargo = scrapy.Field()
	quantity = scrapy.Field()
	ie = scrapy.Field()
	agent = scrapy.Field()

class MovementItem(scrapy.Item):
	date = scrapy.Field()
	state = scrapy.Field()
	vessel_name = scrapy.Field()
	berth_allotted = scrapy.Field()
	pilot_boarding_time = scrapy.Field()

class PositionItem(scrapy.Item):
	date = scrapy.Field()
	berth = scrapy.Field()
	vessel = scrapy.Field()
	ie = scrapy.Field()
	fc = scrapy.Field()
	date_of_berthing = scrapy.Field()
	cargo = scrapy.Field()
	quantity = scrapy.Field()
	day_s_handling = scrapy.Field()
	up_to_date_hanfling = scrapy.Field()
	balance = scrapy.Field()
	load_or_discharge_port = scrapy.Field()
	agent = scrapy.Field()