# -*- codeing = utf-8 -*-
# @Time : 2022/4/3 17:02
# @Author : linyaxuan
# @File : section.py
# @Software : PyCharm


from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import Course, User, CourseType, Section

from common.utils.login_utils import login_required
from common.models import db
from common.model_fields.section_fields import section_fields
from common.utils.custom_output_json import custom_output_json

section_bp = Blueprint('section_bp', __name__)
api = Api(section_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class SectionCRUD(Resource):
    """
    章节的增删改查
    """

    @login_required
    def post(self):
        uid = g.user_id
        user = User.query.get(uid)
        if user.is_superuser != 2:
            return {'code': 403, 'msg': 'This user does not have permission'}
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('video')
        parser.add_argument('cid', type=int)
        args = parser.parse_args()
        for value in args:
            values = args.get(value)
            if len(values) == 0:
                return {'code': 400, 'message': '{} is None'.format(values)}
        course = Course.query.get(args.get('cid'))
        if course:
            section = Section()
            section.title = args.get('title')
            section.video = args.get('video')
            section.cid = args.get('cid')
            db.session.add(section)
            db.session.commit()
            return marshal(course, section_fields)
        return {'code': 500, 'msg': 'Parameter error'}


class GetSection(Resource):
    def get(self):
        section = Section.query.all()
        return marshal(section, section_fields)


class GetVideo(Resource):
    """
    获取视频
    """

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sid')
        args = parser.parse_args()
        sid = args.get('sid')
        video = Section.query.get(sid)
        if video:
            return marshal(video, section_fields)
        return {'code': 400, 'msg': 'Parameter error'}


api.add_resource(GetSection, '/get_section')
api.add_resource(GetVideo, '/get_video')
