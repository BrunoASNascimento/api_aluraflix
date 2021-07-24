from bson import json_util
import json

__all__ = ['delete_one_document']


def delete_one_document(db_handle, id):
    cursor = db_handle.develop.delete_one({'_id': id})
    deleted_count_value = (cursor.deleted_count)

    return deleted_count_value
