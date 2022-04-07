# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : user.py
# @Software : PyCharm
import base64
import hmac
import time
import traceback
import logging
import json
import random
import urllib
import requests
from hashlib import sha256

from common.utils.smstasks import verify_img_code
from common.utils.qny import qn_token
from common.models import db, rds
from common.utils.login_utils import login_required
from common.utils.jwt_utils import _generate_jwt
from common.model_fields.user_fields import user_fields
from common.celery_tasks.main import send_message
from common.utils.captcha import Captcha
from io import BytesIO

from flask import Blueprint, g, make_response, request
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import User, Vip, OtherUser
from sqlalchemy import or_, and_

# 创建蓝图
demo_bp = Blueprint('demo', __name__)
# 实例化蓝图
api = Api(demo_bp)


class Sms(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone')
        args = parser.parse_args()
        mobile = args.get('phone')
        sms_id = random.randint(100000, 999999)
        # send_message(mobile, sms_id)
        sms_code = send_message.delay(mobile, sms_id)
        rds.setex("sms_%s" % mobile, 60 * 5, sms_id)
        # sms_json = json.dumps(sms_code)
        # if sms_json[0] == "000000":
        #     return {"msg": "连接网络超时", "code": "400"}
        return {"msg": "发送成功", "code": "200"}


class ImgCode(Resource):
    def get(self):
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

    @verify_img_code
    def post(self):
        parser = reqparse.RequestParser()
        lis = ['username', 'password']
        for i in lis:
            parser.add_argument(i)
        args = parser.parse_args()
        for value in args:
            values = args.get(value)
            if len(values) == 0:
                return {'code': 400, 'message': '{} is None'.format(values)}
        # code = rds.get(args.get('uuid'))
        # if code is None:
        #     return {'code': 400, 'message': 'Parameter error'}
        # code = code.decode()
        # img_code = args.get('img_code')
        # if img_code.lower() != code.lower():
        #     return {'code': '400', 'message': 'Verification code is not correct'}
        account = args.get('username')
        print(account)
        print(args.get('password'))
        user = User.query.filter(and_(or_(User.account == account, User.phone == account),
                                      User.password == args.get('password'))).first()
        if user:
            user_id = user.uid
            # 生成 token
            token, refresh_token = _generate_jwt(user_id)
            return {'code': 200, 'data': {
                'token': token, 'refresh_token': refresh_token,
                'username': user.account, 'uid': user.uid,
                'img': user.img
            }, 'message': 'login successfully'}
        else:
            return {'code': 400, 'message': 'The account or password is incorrect'}


class OAuthDingding(Resource):
    """
    钉钉回调
    """

    def get(self):
        # code = request.GET.get("code")
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()
        code = args.get('code')
        t = time.time()
        # 时间戳
        timestamp = str((int(round(t * 1000))))
        appSecret = 'Fcah25vIw-koApCVN0mGonFwT2nSze14cEe6Fre8i269LqMNvrAdku4HRI2Mu9VK'
        # 构造签名
        signature = base64.b64encode(
            hmac.new(appSecret.encode('utf-8'), timestamp.encode('utf-8'), digestmod=sha256).digest())
        # 请求接口，换取钉钉用户名
        payload = {'tmp_auth_code': code}
        headers = {'Content-Type': 'application/json'}
        res = requests.post('https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=' + urllib.parse.quote(
            signature.decode("utf-8")) + "&timestamp=" + timestamp + "&accessKey=dingoajf8cqgyemqarekhr",
                            data=json.dumps(payload), headers=headers)
        res_dict = json.loads(res.text)
        unid = res_dict['user_info']['unionid']
        unid = unid[0:12]
        if not unid:
            return {'code': 500, 'msg': res_dict['errmsg']}
        other_user = OtherUser.query.filter_by(unid=unid).first()
        if other_user:
            if other_user.user:
                user = other_user.user
                user = User.query.get(user)
                # 生成 token
                token, refresh_token = _generate_jwt(user.uid)
                return {'code': 200, 'data': {
                    'token': token, 'refresh_token': refresh_token,
                    'username': user.account, 'uid': user.uid,
                    'img': user.img
                }, 'message': 'login successfully'}
        return {'code': 201, 'data': {'unid': unid}}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('unid')
        parser.add_argument('phone')
        parser.add_argument('sms_code')
        args = parser.parse_args()
        phone = args.get('phone')
        sms_code = args.get('sms_code')
        unid = args.get('unid')
        rds_code = rds.get('sms_{}'.format(phone))
        if sms_code != rds_code.decode():
            return {'code': 400, 'msg': 'Parameter error'}
        user = User.query.filter_by(phone=phone).first()
        if user:
            other_user = OtherUser()
            other_user.unid = unid
            other_user.user = user.uid
            other_user.auth_type = '钉钉'
            user_id = user.uid
            db.session.add(other_user)
            db.session.commit()
            # 生成 token
            token, refresh_token = _generate_jwt(user_id)
            return {'code': 200, 'data': {
                'token': token, 'refresh_token': refresh_token,
                'username': user.account, 'uid': user.uid,
                'img': user.img
            }, 'message': 'login successfully'}
        else:
            return {'code': 400, 'message': 'The account or password is incorrect'}


class OAuthWeibo(Resource):
    """
    weibo_callback
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()
        code = args.get('code')
        # 微博认证地址
        access_token_url = "https://api.weibo.com/oauth2/access_token"
        # 返回参数
        # 参数
        res = requests.post(
            access_token_url,
            data={
                "client_id": '4070074327',
                "client_secret": "18e4a3d9b6c6ad4cce096ca2910beed6",
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "http://127.0.0.1:8000/weibo/"
            }
        )


class UserInfo(Resource):
    """
    获取用户信息
    """

    # @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid')
        args = parser.parse_args()
        uid = args.get('uid')
        if uid:
            user = User.query.get(uid)
            return {'code': 200, 'data': {
                'img': user.img, 'username': user.account
            }}


class QiniuToken(Resource):
    def get(self):
        token = qn_token()
        return {"token": token}


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Sms, '/sms_code')
api.add_resource(ImgCode, '/img_code')
api.add_resource(OAuthDingding, '/dingding_back')
api.add_resource(UserInfo, '/user_info')
api.add_resource(QiniuToken, '/get_qnToken')
