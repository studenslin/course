# -*- codeing = utf-8 -*-
# @Author : linyaxuan
# @File : model.py
# @Software : PyCharm

from common.models import db
from datetime import datetime


class User(db.Model):
    """
        用户基本信息
        """
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True, doc='用户ID')
    account = db.Column(db.String(32), doc='账号')
    password = db.Column(db.String(32), doc='密码')
    phone = db.Column(db.String(32), doc='手机号')
    img = db.Column(db.String(500), doc='头像')
    nick_name = db.Column(db.String(32), doc='昵称')
    address = db.Column(db.String(64), doc='地址')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    register_time = db.Column(db.DateTime, doc='注册时间', default=datetime.now)
    is_superuser = db.Column(db.Integer, default=0, doc='0普通用户,1管理员,2超级管理员')
    vip = db.Column(db.Integer, db.ForeignKey("vip.id", ondelete="CASCADE"))
    vip_expiration = db.Column(db.DateTime, doc='vip到期时间')
    other_user = db.relationship('OtherUser', backref=db.backref('other_user'), uselist=False)


class Vip(db.Model):
    __tablename__ = 'vip'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), doc='vip名称')
    level = db.Column(db.Integer, doc='vip等级')
    desc = db.Column(db.String(64), doc='vip描述')
    period = db.Column(db.Integer, default=365, doc='vip有效期')


class OtherUser(db.Model):
    __tablename__ = 'otherUser'
    # Auth_type = (('1', 'weibo'), ('2', 'weixin')) choices=Auth_type
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.uid'), doc='用户id')
    auth_type = db.Column(db.String(32))


class CourseType(db.Model):
    """
    课程类别
    """
    __tablename__ = 'course_type'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), doc='课程类别')
    sequence = db.Column(db.Integer, doc='排序')


class Tag(db.Model):
    """
    课程标签
    """
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), doc='课程标签')
    sequence = db.Column(db.Integer, doc='排序')
    course = db.relationship('Course', secondary='course_tag', backref=db.backref('tags'))


class Course(db.Model):
    """
    课程表
    """
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(24), doc='课程名称')
    desc = db.Column(db.String(256), doc='课程描述')
    img_path = db.Column(db.String(256), doc='课程logo地址')
    course_type = db.Column(db.Integer, db.ForeignKey("course_type.id", ondelete="CASCADE"))
    status = db.Column(db.Integer, doc='课程logo地址', default=0)
    follower = db.Column(db.Integer, default=0, doc='关注人数')
    learner = db.Column(db.Integer, default=0, doc='学习人数')


class CourseTag(db.Model):
    """
    中间表  课程、标签的中间表
    """
    __tablename__ = 'course_tag'
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), primary_key=True, doc='课程id')
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True, doc='标签id')
    is_delete = db.Column(db.Boolean, doc='状态(0存在对应关系;1不存在对应关系)')
