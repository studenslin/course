# -*- codeing = utf-8 -*-
# @Time : 2022/4/9 16:41
# @Author : linyaxuan
# @File : stu_path.py
# @Software : PyCharm

import datetime
import os.path
import random
from alipay import AliPay
from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import Path, Stage, CourseStage, Course

from common.utils.login_utils import login_required
from common.models import rds, db
from common.model_fields.path_fields import path_fields, stage_fields
from common.model_fields.course_fields import courses_fields
from common.utils.custom_output_json import custom_output_json

path_bp = Blueprint('path_bp', __name__)
api = Api(path_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class GetPath(Resource):
    """
    获取路径
    """

    def get(self):
        path = Path.query.all()
        return marshal(path, path_fields)


class HotPath(Resource):
    """
    最热路径
    """

    def get(self):
        path = Path.query.order_by(Path.add_sum.desc()).all()
        path = path[0:5]
        return marshal(path, path_fields)


class PathInfo(Resource):
    """
    路径详情
    """

    def get(self):
        # global courses_list
        parse = reqparse.RequestParser()
        parse.add_argument('pid')
        args = parse.parse_args()
        pid = args.get('pid')

        # 获取路径
        path = Path.query.get(pid)
        if path:

            # 获取阶段
            stages_lis = Stage.query.filter_by(path=pid).all()
            stages = marshal(stages_lis, stage_fields)

            # 阶段对应的课程
            course_data = []
            for stage in stages_lis:
                courses_lis = stage.courses
                courses = marshal(courses_lis, courses_fields)
                course_data.append(courses)

            stages[0]['course_data'] = course_data[0]
            stages[1]['course_data'] = course_data[1]
            stages[2]['course_data'] = course_data[2]
            return {'path_data': marshal(path, path_fields), 'stage_data': stages}
        return {'code': 403, 'msg': 'Parameter error'}


api.add_resource(GetPath, '/get_path')
api.add_resource(HotPath, '/hot_path')
api.add_resource(PathInfo, '/path_info')
