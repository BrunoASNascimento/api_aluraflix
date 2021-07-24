import json
import flask
from flask import request, jsonify
from dotenv import find_dotenv, load_dotenv

from utils_mongodb.mongo_connection import get_db_handle_mongodb
from utils_mongodb.read_documents import get_all_documents, get_one_document
from utils_mongodb.create_document import create_document

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/videos', methods=['GET'])
def list_all_videos():
    db_handle, _ = get_db_handle_mongodb(database_name='study')
    data = get_all_documents(db_handle)
    return jsonify(data)


@app.route('/videos/<int:id>', methods=['GET'])
def get_one_video(id):

    app.logger.info(id)
    db_handle, _ = get_db_handle_mongodb(database_name='study')
    data = get_one_document(db_handle, id)
    return jsonify(data)


@app.route('/videos', methods=['POST'])
def create_video():
    data_request = request.get_json()

    if (data_request.get('titulo') != None) and (data_request.get('descricao') != None) and (data_request.get('url') != None):
        db_handle, _ = get_db_handle_mongodb(database_name='study')
        data = create_document(db_handle, data_request)
        return jsonify(data)
    else:
        error = {}
        return jsonify(error)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    app.run(debug=True)
