from flask import request
from . import api
from ..models import Category, Info
from .. import db
from ..decorators import json, paginate


@api.route('/categories/', methods=['GET'])
@json
@paginate('categories')
def get_categories():
    return Category.query


@api.route('/categories', methods=['POST'])
@json
def new_category():
    category = Category()
    category.import_data(request.json)
    db.session.add(category)
    db.session.commit()
    return {}, 201, {'location': category.get_url()}


@api.route('/categories/<int:id>', methods=['GET'])
@json
def get_category(id):
    return Category.query.get_or_404(id)


@api.route('/categories/<int:id>', methods=['PUT'])
@json
def edit_category(id):
    category = Category.query.get_or_404(id)
    category.import_data(request.json)
    db.session.add(category)
    db.session.commit()
    return {}

@api.route('/categories/<int:id>', methods=['DELETE'])
@json
def delete_categorie(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return {}

@api.route('/infos/<int:id>/categories', methods=['GET'])
@json
@paginate('categories')
def get_info_categories(id):
    info = Info.query.get_or_404(id)
    return info.categories


@api.route('/infos/<int:id>/categories', methods=['POST'])
@json
def add_info_categories(id):
    info = Info.query.get_or_404(id)
    category = Category(info=info)
    category.import_data(request.json)
    db.session.add(category)
    db.session.commit()
    return {}, 201, {'location': category.get_url()}
