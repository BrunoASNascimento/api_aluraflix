from flask import request, jsonify, Flask
import markdown

from utils_mongodb.mongo_connection import get_db_handle_mongodb
from utils_mongodb.read_documents import get_all_documents, get_one_document
from utils_mongodb.create_document import create_document
from utils_mongodb.delete_document import delete_one_document
from utils_mongodb.update_document import update_one_document
from validation_data.validation_document_input import VideoValidation

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    with open('README.md', 'r', encoding='utf-8') as f:
        text = f.read()
        html = f""" 
                <body style="font-family: sans-serif">
                {markdown.markdown(text)}
                </body>
                """
    return html


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
    if data is not None:
        return jsonify(data)
    else:
        return "Não encontrado."


@app.route('/videos', methods=['POST'])
def create_video():
    data_request = request.get_json()

    if (data_request.get('titulo') is not None) and (data_request.get('descricao') is not None) and (data_request.get('url') is not None):
        try:
            VideoValidation(
                data_request.get('titulo'),
                data_request.get('descricao'),
                data_request.get('url')
            )
        except Exception as error:
            return jsonify({
                'error': True,
                'message': str(error)
            })

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

    if data_request.get('id') is None:
        return jsonify({'message': "Não foi encontrado o campo 'id', por favor, inserir.", 'error': True})
    else:
        id_value = data_request['id']
        data_request.pop('id')
        modified_count_value, matched_count = update_one_document(
            db_handle, id_value, data_request)
        if (modified_count_value == 0) and (matched_count == 0):
            return jsonify({'message': 'Videos não encontrado.', 'error': True})
        elif (modified_count_value == 0) and (matched_count > 0):
            return jsonify({'message': 'Video não alterado, todos os campos novos são iguais aos campos anteriores.', 'error': True})
        else:
            data = get_one_document(db_handle, id_value)
            return jsonify(data)


@app.errorhandler(404)
def page_not_found(e):
    url_link = 'https://http.cat/404.png'
    return (f"""
    <body style="background-color:black;">
    <center>
    <img src="{url_link}">
    </center>
    </body>""", 404)


@app.errorhandler(500)
def page_not_found(e):
    url_link = 'https://http.cat/500.png'
    return (f"""
    <body style="background-color:black;">
    <center>
    <img src="{url_link}">
    </center>
    </body>""", 500)
