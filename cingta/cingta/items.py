# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CingtaItem(scrapy.Item):
	title = scrapy.Field()
	date = scrapy.Field()
	url = scrapy.Field()
	type = scrapy.Field()
	source = scrapy.Field()
