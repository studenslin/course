# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : main.py
# @Software : PyCharm

from common.settings.config import Config
from project import create_flask_app

app = create_flask_app(Config)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
