# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : login_utils.py
# @Software : PyCharm
from flask import g
from functools import wraps


def login_required(func):
    # 强制登录
    @wraps(func)
    def wrappers(*args, **kwargs):
        if g.user_id:
            return func(*args, **kwargs)
        return {'code': 500, 'mag': 'err'}
    return wrappers


