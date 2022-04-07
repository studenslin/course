# -*- codeing = utf-8 -*-
# @Time : 2022/3/29 17:29
# @Author : linyaxuan
# @File : course.py
# @Software : PyCharm

from common.utils.login_utils import login_required
from common.models import db
from common.model_fields.section_fields import section_fields
from common.model_fields.course_fields import courses_fields
from common.utils.custom_output_json import custom_output_json

import traceback
import logging

from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import Course, User, CourseType, CourseTag, Section

course_bp = Blueprint('course_bp', __name__)
api = Api(course_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class CourseCRUD(Resource):
    """
    课程的增删改查
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
        parser.add_argument('desc')
        parser.add_argument('img_path')
        parser.add_argument('video')
        parser.add_argument('course_type', type=int)
        args = parser.parse_args()
        try:
            course_type = CourseType.query.get(args.get('course_type'))
            if course_type:
                course = Course()
                course.title = args.get('title')
                course.user = g.user_id
                course.sequence = args.get('sequence')
                course.desc = args.get('desc')
                course.img_path = args.get('img_path')
                course.video = args.get('video')
                course.course_type = args.get('course_type')
                db.session.add(course)
                db.session.commit()
                return marshal(course, courses_fields)
            return {'code': 400, 'msg': 'The title already exists!'}
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
        parser.add_argument('title')
        parser.add_argument('sequence', type=int)
        parser.add_argument('desc')
        parser.add_argument('img_path')
        parser.add_argument('video')
        parser.add_argument('course_type', type=int)
        args = parser.parse_args()
        if CourseType.query.get(args.get('course_type')) is None:
            return {'code': 400, 'msg': 'Parameter error'}
        course_list = Course.query.get(args.get('id'))
        if course_list:
            course_list.title = args.get('title')
            course_list.sequence = args.get('sequence')
            course_list.desc = args.get('desc')
            course_list.img_path = args.get('img_path')
            course_list.video = args.get('video')
            course_list.course_type = args.get('course_type')
            db.session.commit()
            return marshal(course_list, courses_fields)
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
        course = Course.query.get(args.get('id'))
        if course:
            Course.query.filter_by(id=args.get('id')).delete()
            db.session.commit()
            return {'code': 200, 'msg': 'Deleted successfully'}
        return {'code': 500, 'msg': 'Parameter error'}


class GetCourse(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int)
        parser.add_argument('size', type=int)
        parser.add_argument('tag_id')
        parser.add_argument('free')
        parser.add_argument('online')
        args = parser.parse_args()
        page = args.get('page', 1)
        size = args.get('size', 6)
        tag_id = args.get('tag_id')
        free = args.get('free')
        online = args.get('online')
        if tag_id == '' and free == '' and online == '':
            courses = Course.query.order_by(Course.learner).all()
            if courses:
                num = Course.query.count()
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        if free != '' and online != '' and tag_id != '':
            course_tag = CourseTag.query.filter_by(tid=tag_id).first()
            if course_tag:
                cid = course_tag.cid
                courses = Course.query.filter_by(course_type=free, status=online, id=cid).order_by(Course.learner).all()
                num = len(courses)
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        if free == '' and online != '' and tag_id != '':
            course_tag = CourseTag.query.filter_by(tid=tag_id).first()
            if course_tag:
                cid = course_tag.cid
                courses = Course.query.filter_by(status=online, id=cid).order_by(Course.learner).all()
                num = len(courses)
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        if free != '' and online != '' and tag_id == '':
            courses = Course.query.filter_by(course_type=free, status=online).order_by(Course.learner).all()
            if courses:
                num = len(courses)
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        if free != '' and online == '' and tag_id != '':
            course_tag = CourseTag.query.filter_by(tid=tag_id).first()
            if course_tag:
                cid = course_tag.cid
                courses = Course.query.filter_by(course_type=free, id=cid).order_by(Course.learner).all()
                num = len(courses)
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        if free == '' and online != '' and tag_id == '':
            courses = Course.query.filter_by(status=online).order_by(Course.learner).all()
            if courses:
                num = len(courses)
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        if free != '' and online == '' and tag_id == '':
            courses = Course.query.filter_by(course_type=free).order_by(Course.learner).all()
            if courses:
                num = len(courses)
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        if free == '' and online == '' and tag_id != '':
            course_tag = CourseTag.query.filter_by(tid=tag_id).first()
            if course_tag:
                cid = course_tag.cid
                courses = Course.query.filter_by(id=cid).order_by(Course.learner).all()
                num = len(courses)
                start = (page - 1) * size
                end = page * size if num > page * size else num
                courses = courses[start:end]
                return marshal(courses, courses_fields)
            return {'code': 200, 'data': []}
        # return {'code': 400, 'msg': 'Parameter error'}


class CoursersInfo(Resource):
    """
    课程信息
    """

    # @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid')
        args = parser.parse_args()
        cid = args.get('cid')
        course = Course.query.get(cid)
        if course:
            section = Section.query.filter_by(cid=course.id).all()
            return {'code': 200, 'c_data': marshal(course, courses_fields), 's_data': marshal(section, section_fields)}

        return {'code': 400, 'msg': 'Parameter error'}


api.add_resource(CourseCRUD, '/courses')
api.add_resource(GetCourse, '/get_courses')
api.add_resource(CoursersInfo, '/course_info')
