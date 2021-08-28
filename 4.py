import requests
import json
from math import floor
from bs4 import BeautifulSoup
import os


downloads_path = 'downloads/'

headers = {
    'User-agent': 'Mozilla/5.0'
}
access_token = '427c4f24ad053a9e6e82954852d1cd06'
topic_url = f'https://data.gov.ru/api/json/topic?access_token={access_token}'

topics = json.loads(requests.get(topic_url, headers=headers).text)
for i in range(len(topics)):
    topic = topics[i]
    name = topic['name']
    print(f'{i + 1}: {name}')

print()
topic_num = int(input(f'Выберите раздел (1-{len(topics)}): '))
topic_name = topics[topic_num]['name']

datasets = json.loads(
    requests.get(
        f'https://data.gov.ru/api/json/topic/{topic_name}/dataset?access_token={access_token}',
        headers=headers
    ).text
)
datasets_per_page = 20
pages = floor(len(datasets) / datasets_per_page)
page_index = 0


def parse_download_urls(soup: BeautifulSoup):
    anchors = soup.select('div.download a')
    return [(a.text, a['href']) for a in anchors]


def extract_filename(url: str):
    name = url.rsplit('/', 1)[1]
    if '?' in name:
        name = name.split('?')[0]
    return name


while True:
    start = page_index * datasets_per_page
    end = start + datasets_per_page
    if end > len(datasets):
        end = len(datasets)

    for i in range(start, end):
        dataset = datasets[i]
        title = dataset['title']
        print(f'{i + 1}: {title}')

    print(f'\nСтраница {page_index + 1} из {pages}')
    dataset_or_page_num = int(
        input(f'Выберите датасет (от 1 до {len(datasets)}) или страницу (от -1 до -{pages}): ')
    )

    # is dataset
    if dataset_or_page_num > 0:
        dataset = datasets[dataset_or_page_num - 1]
        identifier = dataset['identifier']
        webpage_url = f'https://data.gov.ru/opendata/{identifier}'
        response = BeautifulSoup(requests.get(webpage_url, headers=headers).text, 'lxml')
        variants = parse_download_urls(response)

        for v in range(len(variants)):
            variant_name = variants[v][0]
            print(f'{v + 1}: {variant_name}')

        variant_num = int(input(f'\nВыберите вариант (от 1 до {len(variants)}): '))
        url = variants[variant_num - 1][1]
        filename = extract_filename(url)

        print(f'Загрузка файла {filename}')
        file = requests.get(url)

        if not os.path.exists(downloads_path):
            os.makedirs(downloads_path)
        open(downloads_path + filename, 'wb').write(file.content)
        print(f'Файл загружен')
        break

    # is page
    if dataset_or_page_num < 0:
        page_index = -dataset_or_page_num - 1
