from selenium import webdriver
from pymongo import MongoClient


mongo_client = MongoClient('localhost', 27017)
db = mongo_client['lesson7']

driver = webdriver.Chrome()
driver.implicitly_wait(5)

driver.get('https://onlinetrade.ru')

hit_of_sales_xpath = '//*[@id="main_area"]/div[4]/div/div[7]'
hit_of_sales = driver.find_element_by_xpath(hit_of_sales_xpath)
links_a = hit_of_sales.find_elements_by_css_selector('a.indexGoods__item__name')
links = [a.get_attribute('href') for a in links_a]

for link in links:
    driver.get(link)

    name = driver.find_element_by_css_selector('h1[itemprop="name"]').text
    price_text = driver.find_element_by_css_selector('span[itemprop="price"]').text
    price = int(''.join(filter(str.isdigit, price_text)))

    print(link)
    print(name)
    print(price)

    db.hit_of_sales.update_one(
        {'link': link},
        {'$set': {
            'link': link,
            'name': name,
            'price': price
        }},
        upsert=True
    )

driver.close()
