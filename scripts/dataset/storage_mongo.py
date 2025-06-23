import os
import datetime
from typing import Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.synchronous.collection import Collection

from dataset.models import Entry
from storage import Storage
from dataset.logger import logger


class MongoStore(Storage):
    client = None
    db_name = "mdg"
    entries_collection_name = "entries"

    @property
    def info(self) -> str:
        return f'Mongo Storage'

    def __init__(self):
        self.connect()
        self.database.create_collection("entries", check_exists=False)
        self.entries_collection.create_index([("id", 1)])

    def connect(self):
        username = os.getenv("MONGO_USERNAME", "test_user")
        password = os.getenv("MONGO_PASSWORD", "test_pass")
        host = os.getenv("MONGO_HOST", "127.0.0.1")

        connection_str = f'mongodb://{username}:{password}@{host}/?retryWrites=true&w=majority&appName=newsCollector'

        client = MongoClient(connection_str)
        self.client = client
        logger.info("Connected to mongo database..")

    @property
    def entries_collection(self) -> Collection[Entry]:
        return self.database[self.entries_collection_name]

    @property
    def database(self):
        return self.client[self.db_name]

    def store(self, document: Entry) -> Entry:
        document.stored_at = datetime.datetime.now(
                datetime.UTC).timetuple()
        self.entries_collection.find_one_and_replace({'id': document.id}, document.__dict__)
        logger.info(f"stored document {document.id}")
        return document

    def ping(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"Failed to ping mongo server {e}")
            return False
