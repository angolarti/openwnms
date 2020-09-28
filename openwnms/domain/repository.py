from pymongo import MongoClient
from bson.objectid import ObjectId

import settings
from openwnms.domain import collection


class DB:

    _shared_state = {
        '_client': MongoClient(settings.HOST, settings.PORT)
    }

    def __new__(cls):
        inst = super().__new__(cls)
        inst.__dict__ = cls._shared_state
        return inst


class BaseCollection:

    def collection(self):
        return BaseCollection.document()[self.__class__.__name__.lower()]

    @staticmethod
    def document():
        return DB()._client[settings.DOCUMENT_NAME]

    def to_collection(self):
        return self.__dict__


@collection
class Collection(BaseCollection):

    def __init__(self):
        super().__init__()

        if hasattr(self, '_BaseCollection__document'):
            del self._BaseCollection__document

    def save(self):
        print(type(self.to_collection()))
        return self.collection().insert_one(self.to_collection())

    def update(self):
        return self.collection().update_one(
            {'_id': ObjectId(id)},
            {'$set': self.to_collection()}
        )

    def delete(self):
        self.collection().delete_many({
            '_id': ObjectId(self._id)
        })

    def find_one(self, id: str):
        return self.collection().find_one({
             '_id': ObjectId(id)
        })

    def find_all(self):
        return self.collection().find()

    def list_collections(self, document_name):
        document = self._client[document_name]
        return document.list_collection_names(include_system_collections=False)
