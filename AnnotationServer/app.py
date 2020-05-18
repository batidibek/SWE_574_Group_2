from flask import Flask, request
import service

app = Flask(__name__)


@app.route('/annotations', methods=['POST'])
def new_annotation():
    data = request.get_json()
    response = service.create_annotation(data)
    return response

@app.route('/annotations/<id>', methods=['GET'])
def get_annotation(id):
    response = service.serve_annotation(id)
    return response

@app.route('/annotations/<id>', methods=['PUT'])
def update_annotation(id):
    data = request.get_json()
    response = service.edit_annotation(data, id)
    return response

@app.route('/annotations/<id>', methods=['DELETE'])
def delete_annotation(id):
    service.remove_annotation(id)
    return '', 204