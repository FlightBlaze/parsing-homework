# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from pymongo import MongoClient
from leroymerlin.items import LeroymerlinItem


class LeroymerlinImagesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        urls = item.get(self.files_urls_field, [])
        download_urls = item.get('images', [])
        return [Request(urls[i], meta={'filename': download_urls[i]}) for i in range(len(urls))]

    def file_path(self, request, response=None, info=None):
        return request.meta["filename"]


class LeroymerlinPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.leroymerlin

    def process_item(self, item: LeroymerlinItem, spider):
        collection = self.mongobase[spider.name]
        db_item = {
            'name': item.name,
            'options': item.options,
            'images': item.images
        }
        collection.insert_one(db_item)
        return item
