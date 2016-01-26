# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from threading import Thread, Lock
import MySQLdb
import datetime

app = Flask(__name__)

import os
app.config.from_object(os.environ['APP_SETTINGS'])
api = Api(app)
db = SQLAlchemy(app)
from models import *

class PendingMatch(Resource):

    def get(self,user_phone):
        listOfMatch = list()
        print user_phone
        query = Match.query.join(MatchRow).\
        filter(MatchRow.visitor == user_phone).all()
        if query:
            for row in query:
                dictMatch = dict(
                match_id=row.match_id,
                match_name=row.match_name)
                listOfMatch.append(dictMatch)
        return jsonify({'data': listOfMatch})

api.add_resource(PendingMatch, '/_pending_match/<string:user_phone>')

class AllUser(Resource):

    def get(self):
        listOfUser = list()
        connectQuery = User.query.all()
        if connectQuery:
            for row in connectQuery:
                dictUser = dict(
                     phone=row.phone,
                     user_alias=row.user_alias
                    )
                listOfUser.append(dictUser)
        return jsonify({'data': listOfUser})

api.add_resource(AllUser, '/_all_user')

class UserRegister(Resource):

    def get(self, user_phone, user_alias):
        print user_phone
        print user_alias
        user = User.query.filter_by(phone=user_phone).first()
        if not user:
            db.session.add(
            User(user_phone=user_phone, user_alias=user_alias)
            )
            db.session.commit()
            print "Operacion Correcta"
        return jsonify({'hostping': "culo"})

api.add_resource(UserRegister, '/_user_register/<string:user_phone>/<string:user_alias>')


class NewMatch(Resource):

    def get(self,user_id, match_name, place, visitor):
        print user_id
        print match_name
        print place
        m = Match(user_id, match_name, place)
        mr = MatchRow(visitor=visitor)
        m.match_row.append(mr)
        db.session.add(m)
        db.session.commit()
        return jsonify({'hostping': "culo"})

api.add_resource(NewMatch, '/_new_match/<string:user_id>/<string:match_name>/<string:place>/<string:visitor>')

class ConfirmMatch(Resource):

    def get(self, match_id, user_phone, user_status):
        print match_id
        query = MatchRow.query.filter_by(match_id=match_id).filter_by(visitor=user_phone).first()
        if query:
            print bool(user_status)
            query.visitor_status = bool(user_status)
            db.session.commit()
        return jsonify({'data': user_phone})

api.add_resource(ConfirmMatch, '/_confirm_match/<string:match_id>/<int:user_phone>/<int:user_status>')


@app.route('/')
def index():
    return "Today Match"

if __name__ == '__main__':
    app.run()
