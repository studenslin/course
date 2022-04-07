# -*- codeing = utf-8 -*-
# @Time : 2022/4/6 18:26
# @Author : linyaxuan
# @File : learn.py
# @Software : PyCharm
from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal, fields
from common.models.model import Course, User, CourseType, Section, Comment, Learn

from common.utils.login_utils import login_required
from common.models import db

learn_bp = Blueprint('learn_bp', __name__)
api = Api(learn_bp)

learn_fields = {
    'id': fields.Integer,
    'uid': fields.Integer,
    'sid': fields.Integer,
    'cid': fields.Integer
}


class Learning(Resource):
    @login_required
    def get(self):
        uid = g.user_id
        learn = Learn.query.filter_by(uid=uid).all()
        length = len(learn)
        return {'code': 200, 'data': marshal(learn, learn_fields), 'length': length}


api.add_resource(Learning, '/learn')
