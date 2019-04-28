#coding:utf-8
import scrapy
from cingta.items import CingtaItem
import time
from scrapy.crawler import CrawlerProcess

class cingtaSpider(scrapy.Spider):
	name ='cingtadetail'
	allowed_domains = []

	start_urls = ['https://www.cingta.com/detail/10206/']
	
	#url = 'https://www.cingta.com/detail/%d/'
	#pageNum = 10196

	def parse(self, response):

		item = CingtaItem()
		item['title'] = response.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/p/text()').get().strip()
		item['url'] = response.url
		item['date'] = response.xpath("//span[@class='date']/text()").extract()
		item['type'] = response.xpath("//span[@class='type']/text()").extract()
		
		source_format = response.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/div[2]/p/text()').extract()
		if len(source_format) > 0:
			if '来源' in source_format[-1]:
				item['source'] = source_format[-1]

		
		yield item
		
		#if self.pageNum > 10156:
		#	self.pageNum -= 1
		#	new_url = self.url % self.pageNum
		#	yield scrapy.Request(url=new_url, callback=self.parse)