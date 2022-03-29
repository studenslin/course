# -*- codeing = utf-8 -*-
# @Time : 2022/3/29 16:15
# @Author : linyaxuan
# @File : course_fields.py
# @Software : PyCharm

from flask_restful import fields

course_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'sequence': fields.Integer
}

courses_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'sequence': fields.Integer,
    'desc': fields.String,
    'img_path': fields.String,
    'course_type': fields.String,
    'status': fields.Integer,
    'follower': fields.Integer,
    'learner': fields.Integer,
}
