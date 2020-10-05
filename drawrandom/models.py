from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'item'

    key = db.Column(db.Integer, primary_key=True)
    listkey = db.Column(db.String(), db.ForeignKey('list.key'))
    name = db.Column(db.String(), nullable=False)
    assignee = db.Column(db.String())

    def __init__(self, listkey, name, assignee=None):
        self.listkey = listkey
        self.name = name
        self.assignee = assignee

    def __repr__(self):
        return '<key {}>'.format(self.key)


class List(db.Model):
    __tablename__ = 'list'

    key = db.Column(db.String(), primary_key=True)
    creator = db.Column(db.String(), nullable=False)

    def __init__(self, key, creator):
        self.key = key
        self.creator = creator

    def __repr__(self):
        return '<key {}>'.format(self.key)


