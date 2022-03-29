# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : jwt_utils.py
# @Software : PyCharm

import jwt
from flask import current_app, g
from datetime import datetime, timedelta


def generate_jwt(payload, expiry, secret=None):
    """
    生成 Token
    :param payload: 荷载信息
    :param expiry: 过期时间
    :param secret: 盐
    :return: token
    """
    _payload = {
        'exp': expiry
    }
    _payload.update(payload)

    # 判断是否有盐
    if not secret:
        secret = current_app.config['JWT_SECRET']
    # 生成 Token
    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token


def verify_jwt(token, secret=None):
    """
    校验 Token
    """
    # 判断是否有盐
    if not secret:
        secret = current_app.config['JWT_SECRET']
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except:
        payload = None
    return payload


def _generate_jwt(user_id, refresh=True):
    """
    刷新 token
    :param user_id: 用户 id
    :return:
    """
    secret = current_app.config['JWT_SECRET']
    # 过期时间
    expiry = datetime.utcnow() + timedelta(hours=2)
    # 生成 Token
    token = generate_jwt({'user_id': user_id}, expiry, secret)
    if refresh:
        expiry = datetime.utcnow() + timedelta(days=15)
        refresh_token = generate_jwt({'user_id': user_id, 'is_refresh': True}, expiry, secret)
    else:
        refresh_token = None
    return token, refresh_token


def refresh_token():
    """
    无感刷新 Token
    :return:
    """
    if g.user_id and g.is_refresh is True:
        token, refresh_token = _generate_jwt(g.user_id, refresh=False)
        return {'code': 200, 'data': {'token': token}}
    else:
        return {'code': 500, 'msg': 'token err'}
