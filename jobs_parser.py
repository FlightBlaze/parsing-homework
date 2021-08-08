from bs4 import BeautifulSoup


class Salary:
    def __init__(self, text: str, is_superjob: bool):
        no_price = False
        if len(text) == 0 or is_superjob and text == 'По договорённости':
            no_price = True
            self.price_from = 'N/A'
            self.price_to = 'N/A'
            self.currency = 'руб.'
        elif text.startswith('от'):
            self.price_from = int(''.join(filter(str.isdigit, text)))
            self.price_to = '-'
        elif text.startswith('до'):
            self.price_from = '0'
            self.price_to = int(''.join(filter(str.isdigit, text)))
        elif '–' in text or '—' in text:
            if '–' in text:
                from_to = text.split('–')  # hh.ru
            else:
                from_to = text.split('—')  # superjob.ru
            self.price_from = int(''.join(filter(str.isdigit, from_to[0])))
            self.price_to = int(''.join(filter(str.isdigit, from_to[1])))
        else:
            price = int(''.join(filter(str.isdigit, text)))
            self.price_from = price
            self.price_to = price
        if not no_price:
            chunks = text.split(' ')
            self.currency = chunks[-1]
            if is_superjob:
                self.currency = self.currency.replace('руб./месяц', 'руб.')

    def __str__(self):
        return f"from {self.price_from} to {self.price_to} {self.currency}"


class Vacancy:
    def __init__(self, name, link, salary, company, source):
        self.name = name
        self.link = link
        self.salary = Salary(salary, source == 'superjob.ru')
        self.company = company
        self.source = source

    def __str__(self):
        return f"{self.name}\n{self.company}\n{self.salary.__str__()}\n{self.source}\n{self.link}\n"


def scrap_hh(soup: BeautifulSoup):
    vacancy_divs = soup.find_all(class_='vacancy-serp-item')
    vacancies = []
    for vacancy_div in vacancy_divs:
        anchor = vacancy_div.find(attrs={'data-qa': 'vacancy-serp__vacancy-title'})
        name = anchor.text
        link = anchor['href']
        salary_list = [tag.text.replace('\u202f', ' ') for tag in
                       vacancy_div.find_all(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})]
        company = vacancy_div.find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.replace('\xa0', ' ')
        salary = ''
        if len(salary_list) > 0:
            salary = salary_list[0]
        vacancy = Vacancy(name=name, link=link, salary=salary, company=company, source='hh.ru')
        vacancies.append(vacancy)
    return vacancies


def scrap_superjob(soup: BeautifulSoup):
    vacancy_divs = soup.find_all(class_='Fo44F QiY08 LvoDO')
    vacancies = []
    for vacancy_div in vacancy_divs:
        anchor = vacancy_div.find(class_='_6AfZ9')
        name = anchor.text
        link = 'https://www.superjob.ru' + anchor['href']
        salary = vacancy_div.find(class_='_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW').text.replace('\xa0', ' ')
        company_tag = vacancy_div.find(class_='_205Zx')
        company = 'Anonymous'
        if company_tag is not None:
            company = company_tag.text
        vacancy = Vacancy(name=name, link=link, salary=salary, company=company, source='superjob.ru')
        vacancies.append(vacancy)
    return vacancies
