import requests


apikey = 'beaeb4136be0d5a626653e90f70f9bf6'
query = input("Введите поисковой запрос: ")
url = f'https://gnews.io/api/v4/search?q={query}&token={apikey}'

response = requests.get(url=url)

if not response.ok:
    print("Произошла непредвиденная ошибка")
    exit(0)

with open('search_results.json', 'w', encoding="utf-8") as outfile:
    outfile.write(response.content.decode("utf-8"))

print("Ответ сохранен в файл")
