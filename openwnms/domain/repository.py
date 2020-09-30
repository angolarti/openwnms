from pymongo import MongoClient
from bson.objectid import ObjectId

import settings
from openwnms.domain import collection
from openwnms.tools.utils import current_datetime, last_five_days, ping


class DB:

    _shared_state = {
        '_client': MongoClient(settings.MONGO_URL)
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

    def find_by_mac_addr(self, mac_add: str):
        return self.collection().find_one({
             'mac_addr': mac_add
        })

    def find_all(self):
        return self.collection().find()

    def list_collections(self, document_name):
        document = self._client[document_name]
        return document.list_collection_names(include_system_collections=False)

    def total_devices(self):
        return self.collection().count()

    def find_device_scan_last_five_days(self):
        print('last fives days')
        return self.collection().find({
            'created_at': {
                '$gte': last_five_days(current_datetime()),
                '$lt': current_datetime()
            }
        })

    def count_last_device_scan_last_fine_days(self):
        return self.find_device_scan_last_five_days().count()

    def device_is_up_and_down(self):
        device_up_down = {
            'up': 0,
            'down': 0
        }

        for device in self.find_all():
            if ping(device['ip_addr']):
                device_up_down['up'] += 1
            else:
                device_up_down['down'] += 1

        return device_up_down

    def link_status(self, device):
        print(ping(device['ip_addr']))
        return ping(device['ip_addr'])
