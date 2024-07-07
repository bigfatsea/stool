import pytz
import pymongo
import logging
from datetime import datetime, timedelta
from bson import ObjectId

_logger = logging.getLogger(__name__)

_DB_NAME = 'reeval'
_COLLECTION_NAME = 'status_monitor'

CAT_SERVICE_STATUS = 'service_status'


class StatusMonitor:
    start_timestamp = datetime.now().timestamp()
    status_id = ObjectId()
    stats_id = ObjectId()

    def __init__(self, uri=None):
        if not uri:
            raise ValueError('Missing MongoDB URI')
        self.mdb = pymongo.MongoClient(uri)

    @classmethod
    def new_id(cls):
        return ObjectId()

    def delete(self, id, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        if not id:
            return

        self.mdb[db_name][collection_name].delete_one({'_id': id})

    def save(self, category, data, id=None, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        if not category or not data:
            return

        _logger.info(f'Saving stats for {category}.')
        _id = id if id else self.stats_id
        self.mdb[db_name][collection_name].update_one(
            {'_id': _id},
            {'$set': {**data, 'category': category, 'update_time': datetime.now(pytz.utc)}},
            upsert=True
        )
        _logger.info(f'Saved stats for {category}, id({_id}): {data}\n')

    def delete_status(self, id=None, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        self.delete(id if id else self.status_id, collection_name, db_name)

    def save_status(self, service_name, status='running', id=None, start_timestamp=None,
                    collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        if not service_name or not status:
            return

        if not start_timestamp:
            start_timestamp = self.start_timestamp

        start_time = datetime.fromtimestamp(start_timestamp, tz=pytz.utc)
        data = {'service': service_name, 'status': status, 'start_time': start_time}

        self.save(CAT_SERVICE_STATUS, data, id if id else self.status_id, collection_name, db_name)

    def load(self, category, start=None, end=None, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        if not category:
            return []
        if not start:
            start = datetime.now(pytz.utc) - timedelta(days=7)
        if not end:
            end = datetime.now(pytz.utc)
        condition = {'category': category, 'update_time': {'$gte': start, '$lt': end}}
        result = self.mdb[db_name][collection_name].find(condition)
        return list(result)

    def load_categories(self, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        categories = self.mdb[db_name][collection_name].distinct('category')
        return sorted(categories)


if __name__ == '__main__':
    sm = StatusMonitor()

    sm.save('test', {'a': 1, 'b': 2})
    print('\n'.join([str(x) for x in sm.load('test')]))
    start = datetime.strptime('2024-06-29', "%Y-%m-%d").replace(tzinfo=pytz.utc)
    end = datetime.strptime('2024-07-07', "%Y-%m-%d").replace(tzinfo=pytz.utc)
    statses = sm.load('test', start, end)
    print('\n\t'.join([str(x) for x in statses]))
    categories = sm.load_categories()
    print(categories)
