# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : middlewares.py
# @Software : PyCharm

from common.utils.jwt_utils import verify_jwt
from flask import g, request


def jwt_authentication():
    g.user_id = None
    g.is_refresh = False
    # 获取请求头的 token
    token = request.headers.get('Authorization')
    if token is not None and token.startswith('Bearer '):
        token = token[7:]
        # 验证 token
        payload = verify_jwt(token)
        # 保存到 g 对象
        if payload is not None:
            g.user_id = payload.get('user_id')
            g.is_refresh = payload.get('is_refresh', False)




