class Salary:
    def __init__(self, text: str, is_superjob: bool):

        if not is_superjob:  # hh.ru
            no_price = False
            if text == 'з/п не указана':
                no_price = True
                self.price_from = 'N/A'
                self.price_to = 'N/A'
                self.currency = 'руб.'
            elif 'до' not in text:
                self.price_from = int(''.join(filter(str.isdigit, text)))
                self.price_to = '-'
            elif text.startswith('до'):
                self.price_from = '0'
                self.price_to = int(''.join(filter(str.isdigit, text)))
            elif 'до' in text:
                from_to = text.split('до')
                self.price_from = int(''.join(filter(str.isdigit, from_to[0])))
                self.price_to = int(''.join(filter(str.isdigit, from_to[1])))
            else:
                price = int(''.join(filter(str.isdigit, text)))
                self.price_from = price
                self.price_to = price
            if not no_price:
                chunks = text.split(' ')
                self.currency = chunks[-1]

        else:  # superjob.ru
            no_price = False
            if text is None or text == 'По договорённости':
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
            elif '—' in text:
                from_to = text.split('—')
                self.price_from = int(''.join(filter(str.isdigit, from_to[0])))
                self.price_to = int(''.join(filter(str.isdigit, from_to[1])))
            else:
                price = int(''.join(filter(str.isdigit, text)))
                self.price_from = price
                self.price_to = price
            if not no_price:
                chunks = text.split(' ')
                self.currency = chunks[-1]
                self.currency = self.currency.replace('руб./месяц', 'руб.')

    def __str__(self):
        return f"from {self.price_from} to {self.price_to} {self.currency}"
