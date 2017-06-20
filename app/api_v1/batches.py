from flask import jsonify, request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Batch, Agency


@api.route('/batches', methods=['GET'])
@json
@paginate('batches')
def get_batches():
    return Batch.query

# @api.route('/batches', methods=['POST'])
# @json
# def new_batch():
#     batch = Batch()
#     batch.import_data(request.json)
#     db.session.add(batch)
#     db.session.commit()
#     return {}, 201, {'location': batch.get_url()}

@api.route('/agencies/<int:id>/batches', methods=['GET'])
@json
@paginate('batches')
def get_agency_batches(id):
    agency = Agency.query.get_or_404(id)
    return agency.batches


@api.route('/agencies/<int:id>/batches', methods=['POST'])
@json
def add_agency_batches(id):
    agency = Agency.query.get_or_404(id)
    batch = Batch(agency=agency)
    batch.import_data(request.json)
    db.session.add(batch)
    db.session.commit()
    return {}, 201, {'location': batch.get_url()}

@api.route('/agencies/<int:id>/contacts', methods=['GET'])
@json
@paginate('contacts')
def get_agency_contacts(id):
    agency = Agency.query.get_or_404(id)
    return agency.contacts


@api.route('/agencies/<int:id>/contacts', methods=['POST'])
@json
def add_agency_contacts(id):
    agency = Agency.query.get_or_404(id)
    contact = Contact(agency=agency)
    contact.import_data(request.json)
    db.session.add(batch)
    db.session.commit()
    return {}, 201, {'location': contact.get_url()}


@api.route('/batches/<int:id>', methods=['GET'])
@json
def get_batch(id):
    return Batch.query.get_or_404(id)


@api.route('/batches/<int:id>', methods=['PUT'])
@json
def update_batch(id):
    batch = Batch.query.get_or_404(id)
    batch.import_data(request.json)
    db.session.add(batch)
    db.session.commit()
    return {}


@api.route('/batches/<int:id>', methods=['DELETE'])
@json
def delete_batche(id):
    batch = Batch.query.get_or_404(id)
    db.session.delete(batch)
    db.session.commit()
    return {}
