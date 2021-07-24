from bson import json_util
import json

__all__ = ['update_one_document']


def update_one_document(db_handle, id, data):
    cursor = db_handle.develop.update_one({'_id': id}, {"$set": data})
    modified_count_value = (cursor.modified_count)
    matched_count = (cursor.matched_count)
    return modified_count_value, matched_count
