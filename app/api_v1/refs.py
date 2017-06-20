from flask import jsonify, request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Ref, Info


@api.route('/refs', methods=['GET'])
@json
@paginate('refs')
def get_refs():
    return Ref.query

@api.route('/infos/<int:id>/refs', methods=['GET'])
@json
@paginate('refs')
def get_info_refs(id):
    info = Info.query.get_or_404(id)
    return info.refs


@api.route('/infos/<int:id>/refs', methods=['POST'])
@json
def add_info_refs(id):
    info = Info.query.get_or_404(id)
    ref = Ref(info=info)
    ref.import_data(request.json)
    db.session.add(ref)
    db.session.commit()
    return {}, 201, {'location': ref.get_url()}


@api.route('/refs/<int:id>', methods=['GET'])
@json
def get_ref(id):
    return Ref.query.get_or_404(id)


@api.route('/refs/<int:id>', methods=['PUT'])
@json
def update_ref(id):
    ref = Ref.query.get_or_404(id)
    ref.import_data(request.json)
    db.session.add(ref)
    db.session.commit()
    return {}


@api.route('/refs/<int:id>', methods=['DELETE'])
@json
def delete_ref(id):
    ref = Ref.query.get_or_404(id)
    db.session.delete(ref)
    db.session.commit()
    return {}
