# -*- codeing = utf-8 -*-
# @Time : 2022/3/29 16:13
# @Author : linyaxuan
# @File : courses_type.py
# @Software : PyCharm

from common.utils.login_utils import login_required
from common.models import db
from common.model_fields.course_fields import course_fields
from common.utils.custom_output_json import custom_output_json

import traceback
import logging

from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import CourseType, User

course_type_bp = Blueprint('course_type_bp', __name__)
api = Api(course_type_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class CourseTypeCRUD(Resource):
    """
    课程类别的增删改查
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
            course = CourseType.query.filter_by(title=args.get('title')).first()
            if course:
                return {'code': 400, 'msg': 'The title already exists!'}
            course = CourseType()
            course.title = args.get('title')
            course.sequence = args.get('sequence')
            db.session.add(course)
            db.session.commit()
            return marshal(course, course_fields)
        except:
            error = traceback.format_exc()
            logging.error(error)
            return {'code': 500, 'msg': '{}'.format(error)}

    def get(self):
        try:
            course_list = CourseType.query.order_by().all()
            return marshal(course_list, course_fields)
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
        course_list = CourseType.query.get(args.get('id'))
        if course_list:
            course_list.title = args.get('title')
            course_list.sequence = args.get('sequence')
            db.session.commit()
            return marshal(course_list, course_fields)
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
        course = CourseType.query.get(args.get('id'))
        if course:
            CourseType.query.filter_by(id=args.get('id')).delete()
            db.session.commit()
            return {'code': 200, 'msg': 'Deleted successfully'}
        return {'code': 500, 'msg': 'Parameter error'}


api.add_resource(CourseTypeCRUD, '/course_type', endpoint='course')
