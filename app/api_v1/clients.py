from flask import request, jsonify
from .. import db
from . import api
from ..decorators import json, paginate
from ..models import Client


@api.route('/clients', methods=['GET'])
@json
@paginate('clients')
def get_clients():
    return Client.query


@api.route('/clients', methods=['POST'])
@json
def new_client():
    client = Client()
    client.import_data(request.json)
    db.session.add(client)
    db.session.commit()
    return {}, 201, {'location': client.get_url()}


@api.route('/clients/<int:id>', methods=['GET'])
@json
def get_client(id):
    return Client.query.get_or_404(id)


@api.route('/clients/<int:id>', methods=['PUT'])
@json
def update_client(id):
    client = Client.query.get_or_404(id)
    client.import_data(request.json)
    db.session.add(client)
    db.session.commit()
    return {}


@api.route('/clients/<int:id>', methods=['DELETE'])
@json
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return {}
