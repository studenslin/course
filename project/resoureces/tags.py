# -*- codeing = utf-8 -*-
# @Time : 2022/3/29 17:14
# @Author : linyaxuan
# @File : tags.py
# @Software : PyCharm

from common.utils.login_utils import login_required
from common.models import db
from common.model_fields.tags_fields import tag_fields
from common.utils.custom_output_json import custom_output_json

import traceback
import logging

from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import Tag, User

tags_bp = Blueprint('tags_bp', __name__)
api = Api(tags_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class TagsCRUD(Resource):
    """
    标签的增删改查
    """

    @login_required
    def post(self):
        uid = g.user_id
        user = User.query.get(uid)
        if user.is_superuser != 2:
            return {'code': 403, 'msg': 'This user does not have permission'}
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('sequence', type=int)
        args = parser.parse_args()
        if len(args.get('title')) > 32:
            return {'code': 400, 'msg': 'Parameter error'}
        try:
            tag = Tag.query.filter_by(title=args.get('title')).first()
            if tag:
                return {'code': 400, 'msg': 'The title already exists!'}
            tag = Tag()
            tag.title = args.get('title')
            tag.sequence = args.get('sequence')
            db.session.add(tag)
            db.session.commit()
            return marshal(tag, tag_fields)
        except:
            error = traceback.format_exc()
            logging.error(error)
            return {'code': 500, 'msg': '{}'.format(error)}

    def get(self):
        try:
            tag_list = Tag.query.order_by().all()
            return marshal(tag_list, tag_fields)
        except:
            error = traceback.format_exc()
            logging.error(error)
            return {'code': 500, 'msg': '{}'.format(error)}

    @login_required
    def put(self):
        uid = g.user_id
        user = User.query.get(uid)
        if user.is_superuser != 2:
            return {'code': 403, 'msg': 'This user does not have permission'}
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        parser.add_argument('title')
        parser.add_argument('sequence', type=int)
        args = parser.parse_args()
        if len(args.get('title')) > 32:
            return {'code': 400, 'msg': 'Parameter error'}
        tag_list = Tag.query.get(args.get('id'))
        if tag_list:
            tag_list.title = args.get('title')
            tag_list.sequence = args.get('sequence')
            db.session.commit()
            return marshal(tag_list, tag_fields)
        return {'code': 400, 'msg': 'Parameter error'}

    @login_required
    def delete(self):
        uid = g.user_id
        user = User.query.get(uid)
        if user.is_superuser != 2:
            return {'code': 403, 'msg': 'This user does not have permission'}
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args()
        tag = Tag.query.get(args.get('id'))
        if tag:
            Tag.query.filter_by(id=args.get('id')).delete()
            db.session.commit()
            return {'code': 200, 'msg': 'Deleted successfully'}
        return {'code': 500, 'msg': 'Parameter error'}


api.add_resource(TagsCRUD, '/tags')
