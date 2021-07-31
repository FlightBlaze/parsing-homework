import requests


username = input("Введите имя пользователя GitHub: ")
url = f'https://api.github.com/users/{username}/repos'
response = requests.get(url=url)
if response.status_code == 404:
    print("Такого пользователя не существует")
    exit(0)
elif not response.ok:
    print("Произошла непредвиденная ошибка")
    exit(0)

with open('repos.json', 'w', encoding="utf-8") as outfile:
    outfile.write(response.content.decode("utf-8"))

print("Ответ сохранен в файл")
