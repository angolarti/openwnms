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


@collection
class BaseCollection:

    def __init__(self):
        self.__document = DB()._client.openwnms

    def to_collection(self):
        return self.__dict__


class Collection(BaseCollection):

    def __init__(self):
        self.__document = self._client.openwnms
        self.__collection = self.__document[self.__class__.__name__.lower()]

    def save(self):
        return self.__collection.insert_one(self.to_collection())

    def update(self):
        return self.__collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': self.to_collection()}
        )

    def delete(self):
        self.__collection.delete_many({
            '_id': ObjectId(self._id)
        })

    def find_all(self):
        return self.__collection.find()

    def list_collections(self, document_name):
        document = self._client[document_name]
        return document.list_collection_names(include_system_collections=False)


if __name__ == '__main__':
    model = Collection()

    for col in model.list_collections('flask-mongo'):
        print(col)
