import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlin.items import LeroymerlinItem
from os.path import splitext


def parse_options(response: HtmlResponse):
    options_responses = response.css('.def-list__group')
    options = [(r.css('.def-list__term::text').extract_first(),
                r.css('.def-list__definition::text').extract_first().replace('\n', '').replace('  ', ''))
               for r in options_responses]
    return options


def product_parse(response: HtmlResponse):
    il = ItemLoader(item=LeroymerlinItem(), response=response)

    name_xpath = '/html/body/div[3]/div[2]/div[6]/div[1]/div[2]/div/div/div/div/uc-pdp-card-ga-enriched/h1/text()'
    name = il.get_xpath(name_xpath)
    il.add_value('name', name)

    options = parse_options(response)
    il.add_value('options', options)

    file_urls = il.get_css('img[slot="thumbs"]::attr(src)')
    downloaded_file_urls = [
        f'{name[0].replace("/", "")}/{i}{splitext(file_urls[i])[1]}'
        for i in range(len(file_urls))
    ]
    il.add_value('file_urls', file_urls)
    il.add_value('images', downloaded_file_urls)

    return il.load_item()


class DecorSpider(scrapy.Spider):
    name = 'decor'
    domain_url = 'https://leroymerlin.ru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/dekor/']

    def parse(self, response: HtmlResponse):
        next_page = self.domain_url + response.css('a[data-qa-pagination-item="right"]::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        links = response.css(
            'a[data-qa="product-image"]::attr(href)'
        ).extract()

        for link in links:
            yield response.follow(self.domain_url + link, callback=product_parse)
