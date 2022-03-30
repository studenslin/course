# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : user.py
# @Software : PyCharm
import traceback
import logging
import json

from common.utils.login_utils import login_required
from common.models import db, rds
from common.cache import cache
from common.utils.jwt_utils import _generate_jwt
from common.model_fields.user_fields import user_fields
from common.utils.custom_output_json import custom_output_json
from common.utils.smstasks import send_message
from common.utils.captcha import Captcha

from io import BytesIO

from flask import Blueprint, g, make_response
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import User, Vip

# 创建蓝图
demo_bp = Blueprint('demo', __name__)
# 实例化蓝图
api = Api(demo_bp)


# @api.representation('application/json')
# def output_json(data, code=200, headers=None):
#     return custom_output_json(data, code, headers)


class Sms(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone')
        args = parser.parse_args()
        mobile = args.get('phone')
        print('mobile', mobile)
        sms_code = send_message(mobile)
        sms_json = json.dumps(sms_code)
        if sms_json[0] == "000000":
            return {"msg": "连接网络超时", "code": "400"}
        return {"msg": "发送成功", "code": "200"}


class ImgCode(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('uuid')
            args = parser.parse_args()
            uuid = args.get('uuid')
            text, image = Captcha.gene_graph_captcha()
            rds.setex(uuid, 60 * 5, text)
            out = BytesIO()
            image.save(out, 'png')
            out.seek(0)
            resp = make_response(out.read())
            resp.content_type = 'image/png'
            return resp
        except:
            error = traceback.format_exc()
            logging.error('code image error{}'.format(error))
            return 'fail'


class Register(Resource):
    """
    用户的增删改查
    """

    def post(self):
        parser = reqparse.RequestParser()
        # 添加序列化字段
        lis = ['username', 'password', 'phone', 'code']
        # 添加校验字段
        for i in lis:
            parser.add_argument(i)
        args = parser.parse_args()
        for value in args:
            values = args.get(value)
            print(values)
            if len(values) == 0:
                return {'code': 500, 'msg': '{} is None'.format(values)}
        account = args.get('username')
        if account == User.query.filter_by(account=account).first():
            return {'code': 500, 'msg': 'The account already exists'}
        codes = rds.get('sms_{}'.format(args.get('phone')))
        if args.get('code') != codes.decode():
            return {'code': 400, 'msg': 'Parameter error'}
        user = User()
        user.account = account
        user.password = args.get('password')
        user.phone = args.get('phone')
        db.session.add(user)
        db.session.commit()
        return marshal(user, user_fields)


class Login(Resource):
    """
    登录
    """

    def post(self):
        parser = reqparse.RequestParser()
        lis = ['username', 'password']
        for i in lis:
            parser.add_argument(i)
        args = parser.parse_args()
        for value in args:
            values = args.get(value)
            if len(values) == 0:
                return {'code': 500, 'msg': '{} is None'.format(values)}
        user = User.query.filter_by(account=args.get('username'), password=args.get('password')).first()
        if user:
            user_id = user.uid
            # 生成 token
            token, refresh_token = _generate_jwt(user_id)
            return {'code': 200, 'data': {
                'token': token, 'refresh_token': refresh_token,
                'username': user.account, 'uid': user.uid
            }}
        else:
            return {'code': 200, 'msg': 'The account or password is incorrect'}


# class UserInfo(Resource):
#     """
#     获取所有用户信息
#     """
#
#     @cache.cached(timeout=60)
#     @login_required
#     def get(self):
#         try:
#             uid = g.user_id
#             info = User.query.get(uid)
#             return marshal(info, user_fields)
#         except:
#             return {'code': 500, 'msg': 'err'}


# class UserVip(Resource):
#     """
#     修改vip 等级
#     """
#
#     @login_required
#     def post(self):
#         uid = g.user_id
#         user = User.query.get(uid)
#         if user.is_superuser != 2:
#             return {'code': 403, 'msg': 'This user does not have permission'}
#         parser = reqparse.RequestParser()
#         parser.add_argument('id', type=int)
#         parser.add_argument('vip_id', type=int)
#         args = parser.parse_args()
#         id = args.get('id')
#         vip_id = args.get('vip')
#         user = User.query.get(id)
#         if user:
#             if Vip.query.get(vip_id):
#                 user.vip = vip_id
#                 db.session.commit()
#             return marshal(user, user_fields)
#         return {'code': 400, 'msg': 'Parameter error'}


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
# api.add_resource(UserInfo, '/user_info')
# api.add_resource(UserVip, '/put/user_level')
api.add_resource(Sms, '/sms_code')
api.add_resource(ImgCode, '/img_code')
