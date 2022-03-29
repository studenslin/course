# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : __init__.py.py
# @Software : PyCharm

from flask_sqlalchemy import SQLAlchemy
from common.settings.config import Redis

# 实例化 SQLAlchemy
db = SQLAlchemy()
# 实例化Redis
rds = Redis().connect()
