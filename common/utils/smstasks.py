# # -*- codeing = utf-8 -*-
# # @Time : 2022/3/30 10:08
# # @Author : linyaxuan
# # @File : smstasks.py
# # @Software : PyCharm
#
#
# # 生成短信验证码
# from __future__ import absolute_import, unicode_literals
# from ronglian_sms_sdk import SmsSDK
# from celery import shared_task
# import random
# from common.models import rds
# from common.celery_tasks.main import celery_app
#
#
# accId = "8aaf07087d55e4d9017d6fc4081d0576"
# accToken = "ad66fb53f02949d7bb95c29125a28c5c"
# appId = "8a216da87de15752017dff9ef8c806aa"
#
#
# # @shared_task
# @celery_app.task(name='common.utils.smstasks')
# def send_message(mobile, sms_id):
#     sdk = SmsSDK(accId, accToken, appId)
#     tid = '1'
#     print(sms_id)
#     # sms_id = random.randint(100000, 999999)
#     datas = (sms_id,)
#     rds.setex("sms_%s" % mobile, 60 * 5, sms_id)
#     resp = sdk.sendMessage(tid, mobile, datas)
#     print(resp)
#     return resp


"""
图片验证
"""
from common.models import rds
import json
from functools import wraps
from flask import request


def verify_img_code(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        data = request.data
        data = data.decode()
        data = json.loads(data)
        img_code = data['img_code']
        uuid = data['uuid']
        if uuid is None or img_code is None:
            return {'code': 400, 'message': 'Parameter error'}
        code = rds.get(uuid)
        codes = code.decode()
        print(codes, img_code)
        if codes is None:
            return {'code': 400, 'message': 'Parameter error'}
        if img_code.lower() != codes.lower():
            return {'code': '400', 'message': 'Verification code is not correct'}
        return func(*args, **kwargs)

    return wrappers
