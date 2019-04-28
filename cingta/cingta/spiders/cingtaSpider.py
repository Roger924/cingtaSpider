#coding:utf-8
import scrapy
from cingta.items import CingtaItem
import time
from scrapy.crawler import CrawlerProcess
from goto import with_goto

class cingtaSpider(scrapy.Spider):
	name ='cingta'
	allowed_domains = []

	start_urls = ['https://www.cingta.com/page/1']

	url = 'https://www.cingta.com/page/%d/'
	pageIndex=1
	
	# You should change the crawl max page number here
	pageMax=3
	
	def parse(self, response):
			
		for link in response.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/section/ul/a/@href').extract():
			yield scrapy.Request('https://www.cingta.com'+link, callback=self.parse_details)

		self.pageIndex += 1
		next_url = self.url % self.pageIndex
		if self.pageIndex<self.pageMax:
			yield scrapy.Request(url=next_url,callback=self.parse)
	
	@with_goto	
	def parse_details(self,response):
		item = CingtaItem()
		item['title'] = response.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/p/text()').get().strip()
		item['url'] = response.url
		item['date'] = response.xpath("//span[@class='date']/text()").extract()
		item['type'] = response.xpath("//span[@class='type']/text()").extract()
		
		
		# Different detail pages have different methods for analysis. 
		# I have crawled the data from 2019/1/1-2019/4/28 and only 370 items do not have source(Total num is 2092)
		source_format1 = response.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/div[2]/p/text()').extract()
		if len(source_format1) > 0:
			if '来源' in source_format1[-1]:
				item['source'] = source_format1[-1]
				goto .end
			elif len(source_format1) > 1 and '来源' in source_format1[-2]:
				item['source'] = source_format1[-2]
				goto .end
				
		source_format2 = response.xpath('//strong/text()').extract()
		if len(source_format2) > 0:
			if '来源' in source_format2[-1]:
				item['source'] = source_format2[-1]
				goto .end
				
		source_format3 = response.xpath('//span[@class="bjh-p"]/text()').extract()
		if len(source_format3) > 0:
			if '来源' in source_format3[-1]:
				item['source'] = source_format3[-1]
				goto .end

		source_format4 = response.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/div[2]/div/text()').extract()
		if len(source_format4) > 0:
			if '来源' in source_format4[-1]:
				item['source'] = source_format4[-1]
				goto .end

		source_format5 = response.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/div[2]/div/article/div/p/text()').extract()
		if len(source_format5) > 0:
			if '来源' in source_format5[-1]:
				item['source'] = source_format5[-1]
				goto .end

		source_format6 = response.xpath('//*[@id="blog_article"]/p/text()').extract()
		if len(source_format6) > 0:
			if '来源' in source_format6[-1]:
				item['source'] = source_format6[-1]
				goto .end

		source_format7 = response.xpath('//span[@class="bjh-strong"]/text()').extract()
		if len(source_format7) > 0:
			if '来源' in source_format7[-1]:
				item['source'] = source_format7[-1]
				goto .end
		
		label .end
		yield item