import jobs_parser as parser
from pymongo.database import Database
from pymongo import MongoClient
from fake_headers import Headers
from bs4 import BeautifulSoup
import requests


def add_or_update_vacancy(db: Database, vacancy: parser.Vacancy):
    db.vacancies.update_one(
        {'link': vacancy.link},
        {'$set': {
            'link': vacancy.link,
            'company': vacancy.company,
            'salary': {
                'from': vacancy.salary.price_from,
                'to': vacancy.salary.price_to,
                'currency': vacancy.salary.currency
            },
            'name': vacancy.name,
            'source': vacancy.source
        }},
        upsert=True
    )


headers = Headers(headers=True).generate()

search_query = 'курьер'  # input("Введите поисковый запрос: ")

hh_url = f'https://spb.hh.ru/search/vacancy?text={search_query}'
hh_soup = BeautifulSoup(requests.get(hh_url, headers=headers).text, 'lxml')

superjob_url = f'https://www.superjob.ru/vacancy/search/?keywords={search_query}'
superjob_soup = BeautifulSoup(requests.get(superjob_url, headers=headers).text, 'lxml')

vacancies_ = parser.scrap_hh(hh_soup) + parser.scrap_superjob(superjob_soup)

client = MongoClient('localhost', 27017)
db_ = client['lesson3']

for vacancy_ in vacancies_:
    add_or_update_vacancy(db_, vacancy_)
