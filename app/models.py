from flask import url_for, request
from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from . import db
from .exceptions import ValidationError
from .utils import split_url

class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    batches = db.relationship(
        'Batch',
        backref='agency',
        lazy='dynamic'
    )

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid customer: missing ' + e.args[0])
        return self

    def get_url(self):
        return url_for('api.get_agency', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'batches_url': url_for('api.get_agency_batches', id=self.id, _external=True)
        }

class Batch(db.Model):
    __tablename__ = 'batches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))
    samples = db.relationship(
        'Sample',
        backref='batch',
        lazy='dynamic'
    )

    def get_url(self):
        return url_for('api.get_batch', id=self.id, _external=True)

    def export_data(self):

        return {
            'self_url': self.get_url(),
            'name': self.name,
            'agency_url': self.agency.get_url(),
            'samples_url': url_for('api.get_batch_samples', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid batch: missing ' + e.args[0])
        return self



class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    results = db.relationship(
        'Result',
        backref='sample',
        lazy='dynamic'
    )

    def get_url(self):
        return url_for('api.get_sample', id=self.id, _external=True)

    def export_data(self):
        if self.client != None:
            client_url = self.client.get_url()
        else:
            client_url = ''

        return {
            'self_url': self.get_url(),
            'name': self.name,
            'batch_url': self.batch.get_url(),
            'client_url': client_url,
            'results_url': url_for('api.get_sample_results', id=self.id, _external=True)
        }

    def import_data(self, data):

        try:
            self.name = data['name']
            self.client_url = data['client_url']
        except KeyError as e:
            raise ValidationError('Invalid sample: missing ' + e.args[0])

        if data['client_url'] is not None:
            endpoint, args = split_url(data['client_url'])

            if endpoint != 'api.get_client' or 'id' not in args:
                raise ValidationError('Invalid client url:' + data['client_url'])
            self.client = Client.query.get(args['id'])
            if self.client is None:
                raise ValidationError('Invalid client url:' + data['client_url'])
        return self


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    samples = db.relationship(
        'Sample',
        backref='client',
        lazy='dynamic'
    )

    def get_url(self):
        return url_for('api.get_client', id=self.id, _external=True)

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid client: missing ' + e.args[0])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'samples_url': url_for('api.get_client_samples', id=self.id, _external=True),
            'name': self.name
        }


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.now)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))

    def get_url(self):
        return url_for('api.get_result', id=self.id, _external=True)

    def import_date(self, data):
        try:
            self.name = data['name']
            self.date = datetime_parser.paste(data['date']).astimezone(tzutc()).replace(tzinfo=None)
        except KeyError as e:
            raise ValidationError('Invalid result: missing ' + e.args[0])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'date': self.date.isoformate() + 'Z',
            'sample_url': self.sample.get_url()
        }


