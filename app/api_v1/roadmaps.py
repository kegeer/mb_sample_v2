from flask import jsonify, request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Roadmap


@api.route('/roadmaps', methods=['GET'])
@json
@paginate('roadmaps')
def get_roadmaps():
    return Roadmap.query

@api.route('/roadmaps', methods=['POST'])
@json
def new_roadmap():
    roadmap = Roadmap()
    roadmap.import_data(request.json)
    db.session.add(roadmap)
    db.session.commit()
    return {}, 201, {'location': roadmap.get_url()}

@api.route('/roadmaps/<int:id>', methods=['GET'])
@json
def get_roadmap(id):
    return Roadmap.query.get_or_404(id)

@api.route('/roadmaps/<int:id>', methods=['PUT'])
@json
def update_roadmap(id):
    roadmap = Roadmap.query.get_or_404(id)
    roadmap.import_data(request.json)
    db.session.add(roadmap)
    db.session.commit()
    return {}


@api.route('/roadmaps/<int:id>', methods=['DELETE'])
@json
def delete_roadmap(id):
    roadmap = Roadmap.query.get_or_404(id)
    db.session.delete(roadmap)
    db.session.commit()
    return {}
