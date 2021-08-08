from pymongo.database import Database
from pymongo import MongoClient

threshold = int(input('Введите сумму: '))
client = MongoClient('localhost', 27017)
db = client['lesson3']

results = db.vacancies.find({
    '$or': [
        {'salary.from': {'$gt': threshold}},
        {'salary.to': {'$gt': threshold}}
    ]
})

for doc in results:
    print(doc)
