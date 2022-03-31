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
#
#
#
# accId = "8aaf07087d55e4d9017d6fc4081d0576"
# accToken = "ad66fb53f02949d7bb95c29125a28c5c"
# appId = "8a216da87de15752017dff9ef8c806aa"
#
#
# # @shared_task
#
# def send_message(mobile, sms_id):
#     sdk = SmsSDK(accId, accToken, appId)
#     tid = '1'
#     # sms_id = random.randint(100000, 999999)
#     datas = (sms_id,)
#     resp = sdk.sendMessage(tid, mobile, datas)
#     print(resp)
#     return resp
