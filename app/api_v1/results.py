from flask import request
from .. import db
from ..decorators import json, paginate
from ..models import Sample, Result
from . import api


@api.route('/results', methods=['GET'])
@json
@paginate('clients')
def get_results():
    return Result.query

@api.route('/samples/<int:id>/results', methods=['GET'])
@json
@paginate('results')
def get_sample_results(id):
    sample = Sample.query.get_or_404(id)
    return sample.results


@api.route('/samples/<int:id>/results', methods=['POST'])
@json
def new_sample_result(id):
    sample = Sample.query.get_or_404(id)
    result = Result(sample=sample)
    result.import_date(request.json)
    db.session.add(result)
    db.session.commit()
    return {}, 201, {'location': result.get_url()}


@api.route('/results/<int:id>', methods=['GET'])
@json
def get_result(id):
    return Result.query.get_or_404(id)


@api.route('/results/<int:id>', methods=['PUT'])
@json
def update_result(id):
    result = Result.query.get_or_404(id)
    result.import_data(request.json)
    db.session.add(result)
    db.session.commit()
    return {}


@api.route('/results/<int:id>', methods=['DELETE'])
@json
def delete_result(id):
    result =  Result.query.get_or_404(id)
    db.session.delete(result)
    db.session.commit()
    return {}
