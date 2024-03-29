import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbancatlanItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BbancatlanSpider(scrapy.Spider):
	name = 'bancatlan'
	start_urls = ['https://www.bancatlan.hn/sala-de-prensa/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn btn-primary"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//header[@class="entry-header"]/p/text()').get()
		date = re.findall(r'\d+\s(?:de\s)?\w+(?:\,\s|\s|\sde\s)?\d+', date)
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="news-contenido"]//text()[not (ancestor::blockquote)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=BbancatlanItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
