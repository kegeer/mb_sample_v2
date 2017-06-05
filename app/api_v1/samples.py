from flask import request
from . import api
from .. import db
from ..decorators import json, paginate
from ..models import Sample, Batch, Client


@api.route('/samples', methods=['GET'])
@json
@paginate('samples')
def get_samples():
    return Sample.query


@api.route('/batches/<int:id>/samples', methods=['GET'])
@json
@paginate('samples')
def get_batch_samples(id):
    batch = Batch.query.get_or_404(id)
    return batch.samples


@api.route('/batches/<int:id>/samples', methods=['POST'])
@json
def add_batch_sample(id):
    batch = Batch.query.get_or_404(id)
    sample = Sample(batch=batch)
    sample.import_data(request.json)
    db.session.add(sample)
    db.session.commit()
    return {}, 201, {'location': sample.get_url()}


@api.route('/clients/<int:id>/samples', methods=['GET'])
@json
@paginate('samples')
def get_client_samples(id):
    client = Client.query.get_or_404(id)
    return client.samples


@api.route('/samples/<int:id>', methods=['GET'])
@json
def get_sample(id):
    return Sample.query.get_or_404(id)


@api.route('/samples/<int:id>', methods=['PUT'])
@json
def update_sample(id):
    sample = Sample.query.get_or_404(id)
    sample.import_data(request.json)
    db.session.add(sample)
    db.session.commit()
    return {}


@api.route('/samples/<int:id>', methods=['DELETE'])
@json
def delete_sample(id):
    sample = Sample.query.get_or_404(id)
    db.session.delete(sample)
    db.session.commit()
    return {}