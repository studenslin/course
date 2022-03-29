# -*- codeing = utf-8 -*-
# @Time : 2022/3/29 17:16
# @Author : linyaxuan
# @File : tags_fields.py
# @Software : PyCharm

from flask_restful import fields

tag_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'sequence': fields.Integer
}
