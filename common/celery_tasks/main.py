# -*- codeing = utf-8 -*-
# @Time : 2022/3/31 9:30
# @Author : linyaxuan
# @File : main.py
# @Software : PyCharm

from __future__ import absolute_import, unicode_literals
from ronglian_sms_sdk import SmsSDK

from celery import Celery

celery_app = Celery('mycelery',
                    broker='redis://127.0.0.1:6379/12',  # 任务存放的地方
                    backend='redis://127.0.0.1:6379/13',  # 结果存放的地方
                    )

accId = "8aaf07087d55e4d9017d6fc4081d0576"
accToken = "ad66fb53f02949d7bb95c29125a28c5c"
appId = "8a216da87de15752017dff9ef8c806aa"


@celery_app.task(name='celery_tasks.smstasks')
def send_message(mobile, sms_id):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    datas = (sms_id,)
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)
    return resp

