# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : __init__.py.py
# @Software : PyCharm

from common.cache import cache
from common.models import db
from common.utils.middlewares import jwt_authentication
from project.resoureces.user import demo_bp
from project.resoureces.courses_type import course_type_bp
from project.resoureces.course import course_bp
from project.resoureces.tags import tags_bp
from flask_cors import CORS
from flask_restful import Api
from flask import Flask


def create_flask_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.before_request(jwt_authentication)
    app.register_blueprint(demo_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(course_type_bp)
    db.init_app(app)
    cache.init_app(app)
    CORS(app, resources={r"/*/*": {"origins": "*"}})
    Api(app)
    return app
