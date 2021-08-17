# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from homework.items import JobparserItem
from homework.salary import Salary


def vacancy_parse(response: HtmlResponse):
    name = response.css('h1._1h3Zg.rFbjy::text').extract_first()
    salary_raw = ''.join(response.css('div._3MVeX span._2Wp8I *::text').extract()).replace('\xa0', ' ')
    salary = Salary(salary_raw, is_superjob=True)
    yield JobparserItem(name=name,
                        salary_from=salary.price_from,
                        salary_to=salary.price_to,
                        salary_currency=salary.currency,
                        source='superjob.ru',
                        link=response.url)


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-link-Dalshe::attr(href)').extract_first()
        if next_page is not None:  # После второй страницы отваливается
            yield response.follow(next_page, callback=self.parse)

        links = response.css(
            'a._6AfZ9::attr(href)'
        ).extract()

        for link in links:
            yield response.follow(link, callback=vacancy_parse)
