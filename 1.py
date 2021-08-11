# from fake_headers import Headers
from lxml import html
import pandas as pd
import requests


class Article:
    def __init__(self):
        self.titles = []
        self.sources = []
        self.links = []
        self.dates = []

    def to_data_frame(self):
        return pd.DataFrame({
            "Title": self.titles,
            "Link": self.links,
            "Source": self.sources,
            "Date": self.dates
        })


def parse_yandex_news(root: html.etree.Element):
    article = Article()
    article_xpath = '//article'
    title_elements = root.xpath(f'{article_xpath}/div[1]/div/a')
    article.dates = root.xpath(f'{article_xpath}/div[3]/div[1]/div/span[2]/text()')
    article.sources = root.xpath(f'{article_xpath}/div[3]/div[1]/div/span[1]/a/text()')
    article.titles = [title_element.text_content() for title_element in title_elements]
    article.links = [title_element.get('href') for title_element in title_elements]
    return article


def parse_lenta(root: html.etree.Element):
    article = Article()
    article_xpath = '//*[@id="root"]/*/div/div/*/*/*/section/*'
    article.titles = [title.replace('\xa0', ' ') for title in
                      root.xpath(f'{article_xpath}/a/h3/text()')]
    article.dates = root.xpath(f'{article_xpath}/div/span/text()')
    article.links = ['https://lenta.ru/' + link.get('href') for link in
                     root.xpath(f'{article_xpath}/a[@class="titles"]')]
    article.sources = ['lenta.ru' for title in article.titles]
    return article


def parse_mailru_news(root: html.etree.Element):
    article = Article()
    article_xpath = '//div[contains(@class, "newsitem")]'
    article.titles = root.xpath(f'{article_xpath}/span[2]/a/span/text()')
    article.dates = root.xpath(f'{article_xpath}/div/span[1]/text()')
    article.sources = root.xpath(f'{article_xpath}/div/span[2]/text()')
    article.links = [title.get('href') for title in root.xpath(f'{article_xpath}/span[2]/a')]
    return article


# fake-headers генерирует случайную кодировку, с этим проблемы на сайте Lenta.ru
# headers = Headers(headers=True).generate()

headers = {
    'User-agent': 'Mozilla/5.0'
}

# search_query = input("Введите поисковый запрос: ")

yandex_news = parse_yandex_news(html.fromstring(requests.get('https://yandex.ru/news', headers=headers).text))
lenta = parse_lenta(html.fromstring(requests.get('https://lenta.ru', headers=headers).text))
mailru_news = parse_mailru_news(html.fromstring(requests.get('https://news.mail.ru', headers=headers).text))

# print(len(mailru.titles))
# print(len(mailru.links))
# print(len(mailru.dates))
# print(len(mailru.sources))

df = pd.concat([
    yandex_news.to_data_frame(),
    lenta.to_data_frame(),
    mailru_news.to_data_frame()
], axis=0, ignore_index=True)

pd.set_option('max_colwidth', None)
pd.set_option('max_columns', None)
print(df)

df.to_csv('news.csv')
