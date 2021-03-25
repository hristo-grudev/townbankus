import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import TownbankusItem
from itemloaders.processors import TakeFirst


class TownbankusSpider(scrapy.Spider):
	name = 'townbankus'
	start_urls = ['https://www.townbank.us/content/wintrust/townbank/en/small-business/resources/financial-education.article.0.json?limit=9999999']

	def parse(self, response):
		data = json.loads(response.text)
		for post in data['articles']:
			title = post['title']
			date = post['createdDate']
			url = post['path']
			yield response.follow(url, self.parse_post, cb_kwargs={'title': title, 'date': date})

	def parse_post(self, response, title, date):
		description = response.xpath('//div[@class="article-main"]//text()[normalize-space() and not(ancestor::div[@class="socialsharing-wrapper"] | ancestor::div[@class="articletags section"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=TownbankusItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
