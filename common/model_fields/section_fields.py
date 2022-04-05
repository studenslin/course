# -*- codeing = utf-8 -*-
# @Time : 2022/4/3 17:04
# @Author : linyaxuan
# @File : section_fields.py
# @Software : PyCharm

from flask_restful import fields

section_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'video': fields.String,
}