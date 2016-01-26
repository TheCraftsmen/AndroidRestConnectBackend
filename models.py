from app import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime


class Match(db.Model):

    __tablename__ = "match"

    match_id = db.Column(db.Integer, primary_key=True)
    match_name = db.Column(db.Integer, nullable=True)
    match_date = db.Column(db.Date, default=datetime.date.today())
    match_row = relationship("MatchRow", backref="match")
    place = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer)

    def __init__(self, user_id, match_name, place):
        self.user_id = user_id
        self.match_name = match_name
        self.place = place
        

    def __repr__(self):
        pass

class MatchRow(db.Model):

    __tablename__ = "match_row"

    match_row_id = db.Column(db.Integer, primary_key=True)
    visitor = db.Column(db.Integer, nullable=True)
    visitor_status = db.Column(db.Boolean, nullable=True, default=False)
    match_id = db.Column(db.Integer, ForeignKey('match.match_id'))

    def __init__(self, visitor):
        self.visitor = visitor

    def __repr__(self):
        pass

class User(db.Model):

    __tablename__ = "users"

    phone = db.Column(db.String, primary_key=True)
    user_alias = db.Column(db.String, nullable=False)

    def __init__(self, user_phone, user_alias):
        self.phone = user_phone
        self.user_alias = user_alias
  
    def __repr__(self):
        return '<name {}'.format(self.name)