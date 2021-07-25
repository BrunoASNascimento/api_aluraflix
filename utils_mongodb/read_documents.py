from bson import json_util
import json

__all__ = ['get_all_documents', 'get_one_document']


def get_all_documents(db_handle):
    cursor = db_handle.aluraflix.find({})
    data = (json.dumps(list(cursor), default=json_util.default))
    return json.loads(data)


def get_one_document(db_handle, id):
    cursor = db_handle.aluraflix.find_one({'_id': id})
    data = (json.dumps(cursor, default=json_util.default))
    return json.loads(data)
