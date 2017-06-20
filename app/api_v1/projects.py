from flask import jsonify, request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Project


@api.route('/projects', methods=['GET'])
@json
@paginate('projects')
def get_projects():
    return Project.query

@api.route('/projects', methods=['POST'])
@json
def new_project():
    project = Project()
    project.import_data(request.json)
    db.session.add(project)
    db.session.commit()
    return {}, 201, {'location': project.get_url()}

@api.route('/projects/<int:id>', methods=['GET'])
@json
def get_project(id):
    return Project.query.get_or_404(id)

@api.route('/projects/<int:id>', methods=['PUT'])
@json
def update_project(id):
    project = Project.query.get_or_404(id)
    project.import_data(request.json)
    db.session.add(project)
    db.session.commit()
    return {}


@api.route('/projects/<int:id>', methods=['DELETE'])
@json
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return {}
