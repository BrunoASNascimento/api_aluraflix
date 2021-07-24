import flask
from flask import request, jsonify, send_file
from dotenv import find_dotenv, load_dotenv

from utils_mongodb.mongo_connection import get_db_handle_mongodb
from utils_mongodb.read_documents import get_all_documents, get_one_document
from utils_mongodb.create_document import create_document
from utils_mongodb.delete_document import delete_one_document

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
    if data != None:
        return jsonify(data)
    else:
        return "Não encontrado."


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


@app.route('/videos/<int:id>', methods=['DELETE'])
def delete_one_video(id):
    app.logger.info(id)
    db_handle, _ = get_db_handle_mongodb(database_name='study')
    data = delete_one_document(db_handle, id)
    if data == 0:
        return jsonify({'message': 'Videos não encontrado', 'error': True})
    else:
        return jsonify({'message': f'Video {id} apagado com sucesso', 'error': False})


@app.route('/videos', methods=['PUT', 'PATCH'])
def update_one_video():
    data_request = request.get_json()
    db_handle, _ = get_db_handle_mongodb(database_name='study')

    if data_request.get('id'):
        return jsonify({'message': 'Não foi encontrado o campo "id", por favor, inserir.', 'error': True})
    document = get_one_document(db_handle, data_request['id'])


@app.errorhandler(404)
def page_not_found(e):
    url_link = 'https://http.cat/404.png'
    return (f"""
    <body style="background-color:black;">
    <center>
    <img src="{url_link}">
    </center>
    </body>""", 404)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    app.run(debug=True)
