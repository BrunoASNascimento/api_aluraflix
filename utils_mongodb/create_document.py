from bson import json_util
import json


__all__ = ['create_document']


def get_next_sequence_value(db_handle, collection_name):
    sequence_document = db_handle.counters.find_one_and_update(
        {'_id': collection_name},
        {'$inc': {'sequence_value': 1}}
    )
    if sequence_document.get('sequence_value') != None:
        return sequence_document['sequence_value']
    else:
        db_handle.counters.insert_one(
            {'_id': collection_name, 'sequence_value': 0})
        return 0


def create_document(db_handle, data):
    data['_id'] = get_next_sequence_value(db_handle, 'develop')
    cursor = db_handle.develop.insert_one(data)
    data['id'] = cursor.inserted_id
    data.pop('_id')
    return data
