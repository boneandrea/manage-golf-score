from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


class database:
    def connect_db(self):
        print(os.environ.get("DB_SERVER"))
        print(os.environ.get("DB_PORT"))
        print(os.environ.get("DB_USERNAME"))
        print(os.environ.get("DB_PASSWORD"))
        return MongoClient(os.environ.get('DB_SERVER'),
                           int(os.environ.get('DB_PORT')),
                           username=os.environ['DB_USERNAME'],
                           password=os.environ['DB_PASSWORD'])
