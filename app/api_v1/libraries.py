from flask import jsonify, request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Library


@api.route('/libraries', methods=['GET'])
@json
@paginate('libraries')
def get_libraries():
    return Library.query

@api.route('/libraries', methods=['POST'])
@json
def new_librarie():
    librarie = Library()
    librarie.import_data(request.json)
    db.session.add(librarie)
    db.session.commit()
    return {}, 201, {'location': librarie.get_url()}

@api.route('/libraries/<int:id>', methods=['GET'])
@json
def get_librarie(id):
    return Library.query.get_or_404(id)

@api.route('/libraries/<int:id>', methods=['PUT'])
@json
def update_librarie(id):
    librarie = Library.query.get_or_404(id)
    librarie.import_data(request.json)
    db.session.add(librarie)
    db.session.commit()
    return {}


@api.route('/libraries/<int:id>', methods=['DELETE'])
@json
def delete_librarie(id):
    librarie = Library.query.get_or_404(id)
    db.session.delete(librarie)
    db.session.commit()
    return {}
