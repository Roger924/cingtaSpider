#coding:utf-8
import scrapy
from cingta.items import CingtaItem
from scrapy.crawler import CrawlerProcess
import bs4,re
from goto import with_goto


class cingtaSpider(scrapy.Spider):
	name ='cingta'
	allowed_domains = []

	start_urls = ['https://www.cingta.com/page/1']

	url = 'https://www.cingta.com/page/%d/'
	pageIndex=1
	
	# You should change the crawl max page number here
	pageMax=10
	
	def parse(self, response):
			
		for link in bs4.BeautifulSoup(response.text).select('ul.contentList > a'):
			yield scrapy.Request('https://www.cingta.com'+link.get('href'), callback=self.parse_details)

		self.pageIndex += 1
		next_url = self.url % self.pageIndex
		if self.pageIndex<self.pageMax:
			yield scrapy.Request(url=next_url,callback=self.parse)
	
	@with_goto	
	def parse_details(self,response):
		item = CingtaItem()
		
		title = bs4.BeautifulSoup(response.text).select('p#titleId')
		if len(title) > 0:
			item['title'] = title[0].getText().strip()
			
		item['url'] = response.url
		
		type_idx = 0
		for date_type in bs4.BeautifulSoup(response.text).select('span.bottom_left > span'):
			detail_class = date_type.get('class')
			if len(detail_class) > 0:
				if detail_class[0] == 'date':
					item['date'] = date_type.getText()
				elif detail_class[0] == 'type':
					if type_idx == 0:
						item['source'] = date_type.getText()
					elif type_idx == 1:
						item['type'] = date_type.getText()
					type_idx = type_idx+1
					
		if item['source'] != '青塔':
			goto .end
			
		source = ''
		source_parse = ''
					
		source_format0 = bs4.BeautifulSoup(response.text).select('p.source')
		if len(source_format0) > 0:
			source = source_format0[-1].getText()
			if len(source) > 0:
				source_parse = self.parse_source(source)
				if len(source_parse) > 0:
					item['source'] = source_parse
					goto .end
		
		source_format1 = bs4.BeautifulSoup(response.text).select('div#contentId > p')
		if len(source_format1) > 0:
			source = source_format1[-1].getText()
			if len(source) > 0:
				source_parse = self.parse_source(source)
				if len(source_parse) > 0:
					item['source'] = source_parse
					goto .end
					
		label .end
		yield item

	def parse_source(self, source):
		result = ''
		if '转载' in source:
			source_regex = re.compile(r'转载自：(.*?)。.*')
			regex_result = source_regex.search(source)
			if regex_result:
				result = regex_result[1]
			elif '青塔网原创' in source:
				result = '青塔'
			else:
				result = source
		elif '来源' in source:
			result = source	
		return result
		