# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : migrate.py
# @Software : PyCharm
from common.models.model import *
from common.models import db
from project.main import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()
