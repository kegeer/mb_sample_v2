from flask import url_for, request
from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from . import db
from .exceptions import ValidationError
from .utils import split_url
import json

class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    address = db.Column(db.Text)
    contacts = db.relationship(
        'Contact',
        backref='agency',
        lazy='dynamic'
    )
    batches = db.relationship(
        'Batch',
        backref='agency',
        lazy='dynamic'
    )

    def import_data(self, data):
        try:
            self.name = data['name']
            self.address = data['address']
        except KeyError as e:
            raise ValidationError('Invalid customer: missing ' + e.args[0])
        return self

    def get_url(self):
        return url_for('api.get_agency', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'address': self.address,
            'batches_url': url_for('api.get_agency_batches', id=self.id, _external=True),
            'contacts_url': url_for('api.get_agency_contacts', id=self.id, _external=True)
        }

class Batch(db.Model):
    __tablename__ = 'batches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    diliver_time = db.Column(db.DateTime, default=datetime.now)
    arrive_time = db.Column(db.DateTime, default = datetime.now)
    express_num = db.Column(db.String(30))
    # 入库时间
    store_time = db.Column(db.DateTime, default = datetime.now)
    # 存储位置及温度
    store_position_id = db.Column(db.Integer, db.ForeignKey('store_positions.id'))
    # 所属项目
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    # 技术路线
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'))
    # 备注
    remark = db.Column(db.Text)
    samples = db.relationship(
        'Sample',
        backref='batch',
        lazy='dynamic'
    )

    def get_url(self):
        return url_for('api.get_batch', id=self.id, _external=True)

    def import_data(self, data):
        try:
            self.name = data['name']
            self.agency_url = data['agency_url']
            self.contact_url = data['contact_url']
            self.diliver_time = datetime_parser.paste(data['deliver_time']).astimezone(tzutc()).replace(tzinfo=None)
            self.arrive_time = datetime_parser.paste(data['arrive_time']).astimezone(tzutc()).replace(tzinfo=None)
            self.express_num = data['express_num']
            self.store_time = datetime_parser.paste(data['store_time']).astimezone(tzutc()).replace(tzinfo=None)
            self.store_position_url =  data['store_position_url']
            self.project_url = data['project_url']
            self.roadmap_url = data['roadmap_url']
            self.remark = data['remark']
        except KeyError as e:
            raise ValidationError('Invalid batch: missing ' + e.args[0])

        if data['agency_url'] is not None:
            endpoint, args = split_url(data['agency_url'])

            if endpoint != 'api.get_agency' or 'id' not in args:
                raise ValidationError('Invalid agency url:' + data['agency_url'])
            self.agency = Agency.query.get(args['id'])
            if self.agency is None:
                raise ValidationError('Invalid agency url:' + data['client_url'])
        # if data['contact_url'] is not None:
        #     endpoint, args = split_url(data['contact_url'])
        #
        #     if endpoint != 'api.get_contact' or 'id' not in args:
        #         raise ValidationError('Invalid contact url:' + data['contact_url'])
        #     self.contact = Contact.query.get(args['id'])
        #     if self.contact is None:
        #         raise ValidationError('Invalid contact url:' + data['contact_url'])
        # if data['project_url'] is not None:
        #     endpoint, args = split_url(data['project_url'])
        #
        #     if endpoint != 'api.get_project' or 'id' not in args:
        #         raise ValidationError('Invalid project url:' + data['project_url'])
        #     self.project = Project.query.get(args['id'])
        #     if self.project is None:
        #         raise ValidationError('Invalid project url:' + data['project_url'])
        # if data['roadmap_url'] is not None:
        #     endpoint, args = split_url(data['roadmap_url'])
        #
        #     if endpoint != 'api.get_roadmap' or 'id' not in args:
        #         raise ValidationError('Invalid roadmap url:' + data['roadmap_url'])
        #     self.roadmap = Roadmap.query.get(args['id'])
        #     if self.roadmap is None:
        #         raise ValidationError('Invalid roadmap url:' + data['roadmap_url'])
        return self

    def export_data(self):

        return {
            'self_url': self.get_url(),
            'name': self.name,
            'diliver_time': self.diliver_time,
            'arrive_time': self.arrive_time,
            'express_num': self.express_num,
            'stock_time': self.stock_time,
            'remark': self.remark,
            'agency_url': self.agency.get_url(),
            'contact_url': self.contact.get_url(),
            'stock_position_url': self.stock_position.get_url,
            'project': self.project.get_url,
            'roadmap': self.roadmap.get_url,
            'samples_url': url_for('api.get_batch_samples', id=self.id, _external=True)
        }



class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    pmid = db.Column(db.String(20))
    ori_num = db.Column(db.String(20))
    # 样本类型
    type = db.Column(db.SmallInteger)
    # 样品状态
    status = db.Column(db.SmallInteger)
    # 测序类型
    sequence_method = db.Column(db.SmallInteger)
    primer = db.Column(db.SmallInteger)
    sequencer = db.Column(db.SmallInteger)
    # 文库编号
    library_id = db.Column(db.Integer, db.ForeignKey('libraries.id'))
    results = db.relationship(
        'Result',
        backref='sample',
        lazy='dynamic'
    )

    def get_url(self):
        return url_for('api.get_sample', id=self.id, _external=True)

    def import_data(self, data):
        try:
            self.name = data['name']
            self.client_url = data['client_url']
            self.batch_url = data['batch_url']
            self.pmid = data['pmid']
            self.ori_num = data['ori_num']
            self.type = data['type']
            self.status = data['status']
            self.sequence_method = data['sequence_method']
            self.primer = data['primer']
            self.sequencer = data['sequencer']
            self.library_url = data['library_url']
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


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    gender = db.Column(db.SmallInteger())
    age = db.Column(db.SmallInteger())
    height = db.Column(db.Float)
    width = db.Column(db.Float)

    # 额外信息,包括
    extra = db.Column(db.JSON(), nullable=True)
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
            self.gender = data['gender']
            self.age = data['age']
            self.height = data['height']
            self.width = data['width']
        except KeyError as e:
            raise ValidationError('Invalid client: missing ' + e.args[0])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'samples_url': url_for('api.get_client_samples', id=self.id, _external=True),
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'height': self.height,
            'width': self.width
        }


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.now)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    status = db.Column(db.SmallInteger, default = 0)
    auditor = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.JSON)
    categories = db.relationship(
        'Category',
        secondary='category_samples',
        back_populates='results'
    )

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
            'sample_url': self.sample.get_url(),
            'status': self.status,
            'auditor': self.auditor,
            'content': json.loads(self.content),
            'categories': self.categories
        }


class CategoryResult(db.Model):
    __tablename__ = 'category_samples'
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'))

# 结果分类表
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(20))
    results = db.relationship(
        'Result',
        secondary='category_samples',
        back_populates='categories'
    )
    def get_url(self):
        return url_for('api.get_category', id = self.id, _external=True)

    def import_data(self, data):
        try:
            self,name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid Result: missing' + e.args[0])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'results': self.results
        }


# 项目表
class Project(db.Model):
    __tablename__ = 'projects'
    pass


# 技术路线表
class Roadmap(db.Model):
    __tablename__ = 'roadmaps'
    pass

# 机构联系人
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(30))
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))
    pass


# 存储位置
class Store_position(db.Model):
    __tablename__ = 'stock_positions'
    id = db.Column(db.Integer, autoincrement=True)
    # 冰箱编号
    number = db.Column(db.Integer)
    # 位置
    position = db.Column(db.String(100))
    # 温度
    temp = db.Column(db.Float)

