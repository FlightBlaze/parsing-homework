from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import argparse


arg_parser = argparse.ArgumentParser(description='Mail.ru inbox scraper')
arg_parser.add_argument("login")
arg_parser.add_argument("password")
args = arg_parser.parse_args()

login = args.login
password = args.password

mongo_client = MongoClient('localhost', 27017)
db = mongo_client['lesson7']

driver = webdriver.Chrome()

# Если элемент не найдется, Selenium будет пытаться
# его найти следующие 5 секунд
driver.implicitly_wait(5)

driver.get('https://mail.ru')
username_field = driver.find_element_by_name('login')
username_field.send_keys(login)
username_field.send_keys(Keys.RETURN)
password_field = driver.find_element_by_name('password')
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# Подождем, пока загрузятся элементы. Если элемент не найден,
# selenium подождет 5 секунд и попробует еще раз найти его
driver.find_element_by_css_selector('a.llc.js-letter-list-item')

links = [x.get_attribute('href') for x in
         driver.find_elements_by_css_selector('a.llc.js-letter-list-item')]

for link in links:
    driver.get(link)

    sender = driver.find_element_by_css_selector('span.letter-contact').text
    date = driver.find_element_by_css_selector('div.letter__date').text
    subject = driver.find_element_by_css_selector('h2.thread__subject').text
    content = driver.find_element_by_css_selector('div.letter-body').text

    print(sender)
    print(date)
    print(subject)
    print(content)

    db.inbox.update_one(
        {'link': link},
        {'$set': {
            'link': link,
            'sender': sender,
            'subject': subject,
            'date': date,
            'content': content
        }},
        upsert=True
    )

driver.close()
