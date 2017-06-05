from flask import request
from . import api
from ..models import Agency
from .. import db
from ..decorators import json, paginate


@api.route('/agencies/', methods=['GET'])
@json
@paginate('agencies')
def get_agencies():
    return Agency.query


@api.route('/agencies', methods=['POST'])
@json
def new_agency():
    agency = Agency()
    agency.import_data(request.json)
    db.session.add(agency)
    db.session.commit()
    return {}, 201, {'location': agency.get_url()}


@api.route('/agencies/<int:id>', methods=['GET'])
@json
def get_agency(id):
    return Agency.query.get_or_404(id)


@api.route('/agencies/<int:id>', methods=['PUT'])
@json
def edit_agency(id):
    agency = Agency.query.get_or_404(id)
    agency.import_data(request.json)
    db.session.add(agency)
    db.session.commit()
    return {}