# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : user.py
# @Software : PyCharm

from common.utils.login_utils import login_required
from common.models import db
from common.cache import cache
from common.utils.jwt_utils import _generate_jwt
from common.model_fields.user_fields import user_fields
from common.utils.custom_output_json import custom_output_json

from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import User, Vip

# 创建蓝图
demo_bp = Blueprint('demo', __name__)
# 实例化蓝图
api = Api(demo_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class Register(Resource):
    """
    用户的增删改查
    """

    def post(self):
        parser = reqparse.RequestParser()
        # 添加序列化字段
        lis = ['account', 'nick_name', 'password', 'phone']
        # 添加校验字段
        for i in lis:
            parser.add_argument(i)
        args = parser.parse_args()
        for value in args:
            values = args.get(value)
            print(values)
            if len(values) == 0:
                return {'code': 500, 'msg': '{} is None'.format(values)}
        account = args.get('account')
        if account == User.query.filter_by(account=account).first():
            return {'code': 500, 'msg': 'The account already exists'}
        user = User()
        user.account = account
        user.nick_name = args.get('nick_name')
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
        lis = ['account', 'password']
        for i in lis:
            parser.add_argument(i)
        args = parser.parse_args()
        for value in args:
            values = args.get(value)
            if len(values) == 0:
                return {'code': 500, 'msg': '{} is None'.format(values)}
        user = User.query.filter_by(account=args.get('account'), password=args.get('password')).first()
        if user:
            user_id = user.uid
            # 生成 token
            token, refresh_token = _generate_jwt(user_id)
            return {'code': 200, 'data': {'token': token, 'refresh_token': refresh_token}}
        else:
            return {'code': 200, 'msg': 'The account or password is incorrect'}


class UserInfo(Resource):
    """
    获取所有用户信息
    """

    @cache.cached(timeout=60)
    @login_required
    def get(self):
        try:
            uid = g.user_id
            info = User.query.get(uid)
            return marshal(info, user_fields)
        except:
            return {'code': 500, 'msg': 'err'}


class UserVip(Resource):
    """
    修改vip 等级
    """

    @login_required
    def post(self):
        uid = g.user_id
        user = User.query.get(uid)
        if user.is_superuser != 2:
            return {'code': 403, 'msg': 'This user does not have permission'}
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        parser.add_argument('vip_id', type=int)
        args = parser.parse_args()
        id = args.get('id')
        vip_id = args.get('vip')
        user = User.query.get(id)
        if user:
            if Vip.query.get(vip_id):
                user.vip = vip_id
                db.session.commit()
            return marshal(user, user_fields)
        return {'code': 400, 'msg': 'Parameter error'}


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(UserInfo, '/user_info')
api.add_resource(UserVip, '/put/user_level')
