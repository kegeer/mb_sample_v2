from flask import jsonify, request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Info, Category


@api.route('/infos', methods=['GET'])
@json
@paginate('infos')
def get_infos():
    return Info.query

@api.route('/infos', methods=['POST'])
@json
def new_info():
    info = Info()
    info.import_data(request.json)
    db.session.add(info)
    db.session.commit()
    return {}, 201, {'location': info.get_url()}

@api.route('/categories/<int:id>/infos', methods=['GET'])
@json
@paginate('infos')
def get_category_infos(id):
    category = Category.query.get_or_404(id)
    return category.infos


@api.route('/categories/<int:id>/infos', methods=['POST'])
@json
def add_category_infos(id):
    category = Category.query.get_or_404(id)
    info = Info(category=category)
    info.import_data(request.json)
    db.session.add(info)
    db.session.commit()
    return {}, 201, {'location': info.get_url()}


@api.route('/infos/<int:id>', methods=['GET'])
@json
def get_info(id):
    return Info.query.get_or_404(id)


@api.route('/infos/<int:id>', methods=['PUT'])
@json
def update_info(id):
    info = Info.query.get_or_404(id)
    info.import_data(request.json)
    db.session.add(info)
    db.session.commit()
    return {}


@api.route('/infos/<int:id>', methods=['DELETE'])
@json
def delete_info(id):
    info = Info.query.get_or_404(id)
    db.session.delete(info)
    db.session.commit()
    return {}
