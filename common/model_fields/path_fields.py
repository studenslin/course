# -*- codeing = utf-8 -*-
# @Time : 2022/4/9 16:57
# @Author : linyaxuan
# @File : path_fields.py
# @Software : PyCharm


from flask_restful import fields

path_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'img': fields.String,
    'desc': fields.String,
    'section_sum': fields.Integer,
    'add_sum': fields.Integer,
    'study_time': fields.Integer
}

stage_fields = {
    'id': fields.Integer,
    'stage': fields.String,
    'stage_name': fields.String
}