from flask import request, url_for
from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from . import db
from .exceptions import ValidationError
from .utils import split_url
import json

# 合作单位表格
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
            raise ValidationError('Invalid agency: missing' + e.args[0])
        return self

    def get_url(self):
        return url_for('api.get_agency', id=self.id)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'address': self.address,
            'batches_url': url_for('api.get_agency_batches', id=self.id),
            'contacts_url': url_for('api.get_agency_contacts', id=self.id)
        }

# 批次
class Batch(db.Model):
    __tablename__ = 'batches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    deliver_time = db.Column(db.DateTime, default=datetime.now)
    arrive_time = db.Column(db.DateTime, default = datetime.now)
    express_num = db.Column(db.String(30))
    # 入库时间
    store_time = db.Column(db.DateTime, default = datetime.now)
    # 存储位置及温度
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
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
            # self.agency_id = data['agency_id']
            # self.contact_id = data['contact_id']
            self.deliver_time = data['deliver_time']
            self.arrive_time = data['arrive_time']
            self.express_num = data['express_num']
            self.store_time = data['store_time']
            # self.position_id = data['position_id']
            # self.project_id = data['project_id']
            # self.roadmap_id = data['roadmap_id']
            self.remark = data['remark']
        except KeyError as e:
            raise ValidationError('Invalid batch: missing' + e.args[0])
        if data['agency_id'] is not None:
            self.agency = Agency.query.get(data['agency_id'])
        if data['contact_id'] is not None:
            self.contact = Contact.query.get(data['contact_id'])
        if data['position_id'] is not None:
            self.position = Position.query.get(data['position_id'])
        if data['project_id'] is not None:
            self.project = Project.query.get(data['project_id'])
        if data['roadmap_id'] is not None:
            self.roadmap = Roadmap.query.get(data['roadmap_id'])
        return self

    def export_data(self):
        return {
        'self_url': self.get_url(),
        'name': self.name,
        'deliver_time': self.deliver_time,
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

# 样品表
class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
            # self.batch_id = data['batch_id']
            # self.client_id = data['client_id']
            self.pmid = data['pmid']
            self.ori_num = data['ori_num']
            self.type = data['type']
            self.status = data['status']
            self.sequence_method = data['sequence_method']
            self.primer = data['primer']
            self.sequencer = data['sequencer']
            # self.library_id = data['library_id']
        except KeyError as e:
            raise ValidationError('Invalid sample: missing' + e.args[0])
        if data['batch_id'] is not None:
            self.batch = Batch.query.get(data['batch_id'])
        if data['client_id'] is not None:
            self.client = Client.query.get(data['client_id'])
        if data['library_id'] is not None:
            self.library = Library.query.get(data['library_id'])
        return self

    def export_data(self):
        return {
        'batch': self.batch.get_url() if self.batch is not None else '',
        'client_id': self.client.get_url() if self.client is not None else '',
        'pmid': self.pmid,
        'ori_num': self.ori_num,
        'type': self.type,
        'status': self.status,
        'sequence_method': self.sequence_method,
        'primer': self.primer,
        'sequencer': self.sequencer,
        'library_id': self.library.get_url() if self.library is not None else ''
        }

# 客户表
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    gender = db.Column(db.SmallInteger())
    age = db.Column(db.SmallInteger())
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    # 额外信息,包括各项指标
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
            self.extra = data['extra']
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
            'weight': self.width,
            'extra': self.extra
        }

# 结果表
class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.now)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    # 结果状态: 未出具, 未审核, 已出具
    status = db.Column(db.SmallInteger, default = 0)
    # 审核员: 按理说是角色为审核元的人
    auditor = db.Column(db.String(10))
    content = db.Column(db.JSON)

    def get_url(self):
        return url_for('api.get_result', id=self.id, _external=True)

    def import_date(self, data):
        try:
            self.date = datetime_parser.paste(data['date']).astimezone(tzutc()).replace(tzinfo=None)
            self.status = data['status']
            self.auditor = data['auditor']
            self.content = data['content']
        except KeyError as e:
            raise ValidationError('Invalid result: missing' + e.args[0])
        if data['sample_id'] is not None:
            self.sample = Sample.query.get(data['sample_id'])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'date': self.date.isoformate() + 'Z',
            'sample_url': self.sample.get_url(),
            'status': self.status,
            'auditor': self.auditor,
            'content': json.loads(self.content)
        }

# 静态表,存储数据指标
class Info(db.Model):
    __tablename__ = 'infos'
    id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(255), nullable=True)
    e_name = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(50), nullable=True)
    desc = db.Column(db.Text(), nullable=True)
    ref_min = db.Column(db.Float, nullable=True)
    ref_max = db.Column(db.Float, nullable=True)
    alias = db.Column(db.String(50), nullable=True)
    refs = db.relationship(
        'Ref',
        backref='info',
        lazy='dynamic'
    )
    categories = db.relationship(
        'Category',
        secondary='category_infos',
        back_populates='infos'
    )

    def get_url(self):
        return url_for('api.get_info', id=self.id, _external=True)

    def import_data(self, data):
        self.c_name = data['c_name']
        self.e_name = data['e_name']
        self.type = data['type']
        self.desc = data['desc']
        self.ref_min = data['ref_min']
        self.ref_max = data['ref_max']
        self.alias = data['alias']

    def export_data(self):
        return {
        'self_url': self.get_url(),
        'c_name': self.c_name,
        'e_name': self.e_name,
        'type': self.type,
        'desc': self.desc,
        'ref_min': self.ref_min,
        'ref_max': self.ref_max,
        'alias': self.alias,
        'refs': url_for('api.get_info_refs', id=self.id, _external=True),
        'categories': url_for('api.get_info_categories', id=self.id, _external=True)
        }

class CategoryInfo(db.Model):
    __tablename__ = 'category_infos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    info_id = db.Column(db.Integer, db.ForeignKey('infos.id'))

# 分类表, 存储数据的分类
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20))
    infos = db.relationship(
        'Info',
        secondary='category_infos',
        back_populates='categories'
    )
    def get_url(self):
        return url_for('api.get_category', id = self.id, _external=True)

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid Result: missing' + e.args[0])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'infos': url_for('api.get_category_infos', id=self.id, _external=True)
        }
# 结果参考表
class Ref(db.Model):
    __tablename__ = 'refs'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    info_id = db.Column(db.Integer, db.ForeignKey('infos.id'))
    status = db.Column(db.SmallInteger)
    color = db.Column(db.SmallInteger)
    img = db.Column(db.SmallInteger)
    desc = db.Column(db.Text)

    def get_url(self):
        return url_for('api.get_library', id=self.id, _external=True)

    def import_data(self, data):
        try:
            self.status = data['status']
            self.color = data['color']
            self.img = data['img']
            self.desc = data['desc']
        except KeyError as e:
            raise ValidationError('Invalid library: missing' + e.args[0])
        if data['info_id'] is not None:
            self.info = Info.query.get(data['info_id'])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'status': self.status,
            'color': self.color,
            'img': self.img,
            'desc': self.desc,
            'info_url': self.info.get_url()
        }

# 项目表
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def get_url(self):
        return url_for('api.get_project', id=self.id, _external=True)
    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid project: missing' + e.args[0])
        return self
    def export_data(self):
        return {
        'self_url': self.get_url(),
        'name': self.name
        }

# 技术路线
class Roadmap(db.Model):
    __tablename__ = 'roadmaps'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def get_url(self):
        return url_for('api.get_roadmap', id=self.id, _external=True)
    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid roadmap: missing' + e.args[0])
        return self
    def export_data(self):
        return {
        'self_url': self.get_url(),
        'name': self.name
        }


# 联系人表
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, autoincrement=True, primary_key=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))

    def get_url(self):
        return url_for('api.get_contact', id=self.id, _external=True)
    def import_data(self, data):
        try:
            self.name = data['name']
            self.phone = data['phone']
            self.email = data['email']
        except KeyError as e:
            raise ValidationError('Invalid contact: missing' + e.args[0])
        if data['agency_id'] is not None:
            self.agency = Agency.query.get(data['agency_id'])
        return self
    def export_data(self):
        return {
        'self_url': self.get_url(),
        'name': self.name,
        'agency_url': self.agency.get_url()
        }


# 存储位置表
class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def get_url(self):
        return url_for('api.get_position', id=self.id, _external=True)
    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid position: missing' + e.args[0])
        return self
    def export_data(self):
        return {
        'self_url': self.get_url(),
        'name': self.name
        }


# DNA文库表
class Library(db.Model):
    __tablename__ = 'libraries'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def get_url(self):
        return url_for('api.get_library', id=self.id, _external=True)
    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid library: missing' + e.args[0])
        return self
    def export_data(self):
        return {
        'self_url': self.get_url(),
        'name': self.name
        }
