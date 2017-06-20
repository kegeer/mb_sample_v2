from flask import request
from . import api
from ..models import Contact, Info
from .. import db
from ..decorators import json, paginate


@api.route('/contacts/', methods=['GET'])
@json
@paginate('contacts')
def get_contacts():
    return Contact.query

@api.route('/contacts/<int:id>', methods=['GET'])
@json
def get_contact(id):
    return Contact.query.get_or_404(id)


@api.route('/contacts/<int:id>', methods=['PUT'])
@json
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    contact.import_data(request.json)
    db.session.add(contact)
    db.session.commit()
    return {}

@api.route('/contacts/<int:id>', methods=['DELETE'])
@json
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return {}

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
    db.session.add(contact)
    db.session.commit()
    return {}, 201, {'location': contact.get_url()}
