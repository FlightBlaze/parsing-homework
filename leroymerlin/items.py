# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    options = scrapy.Field()
    file_urls = scrapy.Field()
    images = scrapy.Field()
    files = scrapy.Field()
