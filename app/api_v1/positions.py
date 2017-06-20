from flask import jsonify, request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Position


@api.route('/positions', methods=['GET'])
@json
@paginate('positions')
def get_positions():
    return Position.query

@api.route('/positions', methods=['POST'])
@json
def new_position():
    position = Position()
    position.import_data(request.json)
    db.session.add(position)
    db.session.commit()
    return {}, 201, {'location': position.get_url()}

@api.route('/positions/<int:id>', methods=['GET'])
@json
def get_position(id):
    return Position.query.get_or_404(id)

@api.route('/positions/<int:id>', methods=['PUT'])
@json
def update_position(id):
    position = Position.query.get_or_404(id)
    position.import_data(request.json)
    db.session.add(position)
    db.session.commit()
    return {}


@api.route('/positions/<int:id>', methods=['DELETE'])
@json
def delete_position(id):
    position = Position.query.get_or_404(id)
    db.session.delete(position)
    db.session.commit()
    return {}
