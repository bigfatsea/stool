import os

import pymongo
import logging
import pytz
from dateutil import parser as dateutil_parser
from datetime import datetime, timedelta
from bson import ObjectId

_logger = logging.getLogger(__name__)

_DB_NAME = 'reeval'
_COLLECTION_NAME = 'status_monitor'

CAT_SERVICE_STATUS = 'service_status'


class StatusMonitor:

    def __init__(self, uri=None):
        if not uri:
            raise ValueError('Missing MongoDB URI')
        self.mdb = pymongo.MongoClient(uri)

        self.start_timestamp = datetime.now().timestamp()
        self.status_id = ObjectId()
        self.stats_id = ObjectId()

    @classmethod
    def new_id(cls):
        return ObjectId()

    def delete(self, id=None, category=None, start=None, end=None, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        delete_condition = {}
        if end:
            try:
                start_date = start if start else datetime.now(pytz.utc) - timedelta(days=365)
                if not isinstance(start_date, datetime):
                    start_date = dateutil_parser.parse(start_date)
                if not start_date.tzinfo:
                    start_date = start_date.replace(tzinfo=pytz.utc)
                end_date = end
                if not isinstance(end_date, datetime):
                    end_date = dateutil_parser.parse(end_date)
                if not end_date.tzinfo:
                    end_date = end_date.replace(tzinfo=pytz.utc)
                delete_condition['update_time'] = {'$gte': start_date, '$lt': end_date}
            except Exception as e:
                _logger.error(f'Failed to parse start/end time: {e}')

        if id:
            try:
                _id = id if isinstance(id, ObjectId) else ObjectId(id)
                delete_condition['_id'] = _id
            except Exception as e:
                _logger.error(f'Failed to parse id: {e}')

        if category:
            delete_condition['category'] = category

        if delete_condition:
            result = self.mdb[db_name][collection_name].delete_many(delete_condition)
            _logger.info(f'Deleted {result.deleted_count} status/stats with condition: {delete_condition}\n')
        else:
            _logger.info('No condition specified for deletion.\n')

    def save(self, category, data, id=None, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        if not category or not data:
            return

        # _logger.info(f'Saving status/stats for {category}.')
        _id = id if id else self.stats_id
        self.mdb[db_name][collection_name].update_one(
            {'_id': _id},
            {'$set': {**data, 'category': category, 'update_time': datetime.now(pytz.utc)}},
            upsert=True
        )
        _logger.info(f'Saved status/stats for {category}, id({_id}): {data}')

    def delete_status(self, id=None, collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        self.delete(id=id if id else self.status_id, collection_name=collection_name, db_name=db_name)

    def save_status(self, service_name, status='running', id=None, start_timestamp=None,
                    collection_name=_COLLECTION_NAME, db_name=_DB_NAME):
        if not service_name or not status:
            return

        if not start_timestamp:
            start_timestamp = self.start_timestamp

        _id = id if id else self.status_id
        data = {'service': service_name, 'status': status}

        if not self.mdb[db_name][collection_name].find_one({'_id': _id}):  # not exists, insert with start time
            data['start_time'] = datetime.fromtimestamp(start_timestamp, tz=pytz.utc)

        self.save(CAT_SERVICE_STATUS, data, _id, collection_name, db_name)

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
    print('This is a module file, do not run it directly.')
    # sm = StatusMonitor(os.getenv('MONGO_URI'))
    # id = ObjectId('60d2f7d5c2b9e4e1b3d7b2a3')
    # records = sm.load(category='yfinance')
    # print(f'Loaded {len(records)} records.')
    # # print('\n'.join([str(x) for x in records]))
    # sm.delete(id=id)
    # sm.delete(end='2024-07-07')
    # records = sm.load(category='yfinance')
    # print(f'Loaded {len(records)} records.')
    # print('\n'.join([str(x) for x in records]))
    #
    # sm.save('test', {'a': 1, 'b': 2})
    # print('\n'.join([str(x) for x in sm.load('test')]))
    # start = datetime.strptime('2024-06-29', "%Y-%m-%d").replace(tzinfo=pytz.utc)
    # end = datetime.strptime('2024-07-07', "%Y-%m-%d").replace(tzinfo=pytz.utc)
    # statses = sm.load('test', start, end)
    # print('\n\t'.join([str(x) for x in statses]))
    # categories = sm.load_categories()
    # print(categories)
