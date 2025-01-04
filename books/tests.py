from django.test import TestCase
from pymongo import MongoClient


class BookTests(TestCase):
    def setUp(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client["test_database"]
        self.db.books.insert_many([
            {"title": "Book 1", "author": "Author 1", "published_date": "2022-01-01", "genre": "Fiction", "price": 10.0},
            {"title": "Book 2", "author": "Author 2", "published_date": "2022-01-01", "genre": "Non-Fiction", "price": 15.0},
        ])

    def test_average_price(self):
        pipeline = [
            {"$match": {"published_date": {"$regex": "^2022"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
        ]
        result = list(self.db.books.aggregate(pipeline))
        self.assertEqual(result[0]["average_price"], 12.5)

    def tearDown(self):
        self.db.books.drop()