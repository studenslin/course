# -*- codeing = utf-8 -*-
# @Time : 2022/4/2 15:25
# @Author : linyaxuan
# @File : qny.py
# @Software : PyCharm
from qiniu import Auth

# AK,SK
access_key = 'ZxuCr1dxnenWx0-gGIBZcxOMcjytXtZISwgix36L'
secret_key = 'SJl9JmW7zB0j1xHlDPmyjTwJf5E7ksoQicqIDQT8'


# 构建鉴权对象
def qn_token():
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'courses1'
    # 生成上传token
    token = q.upload_token(bucket_name)
    return token
