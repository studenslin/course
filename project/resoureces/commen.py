# -*- codeing = utf-8 -*-
# @Time : 2022/4/6 15:09
# @Author : linyaxuan
# @File : commen.py
# @Software : PyCharm
import json

from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal, fields
from common.models.model import Course, User, CourseType, Section, Comment

from common.utils.login_utils import login_required
from common.models import db
from common.model_fields.commen_fields import comment_fields
from common.model_fields.user_fields import user_fields
from common.utils.custom_output_json import custom_output_json

comment_bp = Blueprint('comment_bp', __name__)
api = Api(comment_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


# data_fields = {
#     'id': fields.Integer,
#     'content': fields.String,
#     'create_time': fields.DateTime,
#     'top': fields.Integer,
#     'uid': fields.Integer,
#     'account': fields.String,
#     'img': fields.String,
# }


class CommentsCRUD(Resource):
    """
    评论
    """

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid')
        parser.add_argument('sid')
        parser.add_argument('content')
        parser.add_argument('reply')
        args = parser.parse_args()
        cid = args.get('cid')
        sid = args.get('sid')
        content = args.get('content')
        reply = args.get('reply')
        uid = g.user_id
        print('222', content)
        print('1111', cid, uid, sid, reply)
        course = Course.query.get(cid)
        if course is None:
            return {'code': 400, 'msg': 'Parameter error'}
        if sid:
            section = Section.query.get(sid)
            if section:
                comment = Comment()
                comment.sid = sid
                comment.cid = cid
                comment.uid = uid
                comment.reply = reply
                comment.content = content
                db.session.add(comment)
                db.session.commit()
                return marshal(comment, comment_fields)
            return {'code': 400, 'msg': 'Parameter error'}
        comment = Comment()
        comment.sid = sid
        comment.cid = cid
        comment.uid = uid
        comment.content = content
        comment.reply = reply
        db.session.add(comment)
        db.session.commit()
        return marshal(comment, comment_fields)

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid')
        parser.add_argument('sid')
        args = parser.parse_args()
        cid = args.get('cid')
        sid = args.get('sid')
        print(cid, sid)
        course = Course.query.get(cid)
        if course is None:
            return {'code': 400, 'msg': 'Parameter error'}
        comment_list = Comment.query.filter_by(cid=cid, uid=g.user_id).all()
        lis = []
        comments = marshal(comment_list, comment_fields)
        for k in comment_list:
            uid = k.uid
            comment_id = k.id
            user = User.query.get(uid)
        child_list = Comment.query.filter_by(cid=cid, reply= comment_id).all()
        for comment in comments:
            comment.update({
                'child_list': marshal(child_list, comment_fields),
                'user_info': {
                    'username': user.account,
                    'img': user.img,
                    'uid': user.uid,
                }
            })
            lis.append(comment)

        return lis


api.add_resource(CommentsCRUD, '/comments')
