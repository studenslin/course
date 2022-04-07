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
    other_user = db.relationship('OtherUser', backref='auth')


class Vip(db.Model):
    __tablename__ = 'vip'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), doc='vip名称')
    level = db.Column(db.Integer, doc='vip等级(普通会员,高级会员)')
    price = db.Column(db.DECIMAL(20, 2), doc='会员价格')
    desc = db.Column(db.String(64), doc='vip描述')
    period = db.Column(db.Integer, default=365, doc='vip有效期')
    exempt_cour = db.Column(db.Integer, doc='免费课程{0或空:不享受,1:享受}')
    vip_cour = db.Column(db.Integer, doc='会员课程{0或空:不享受,1:享受}')
    environment = db.Column(db.Integer, doc='实验环境联网{0或空:不享受,1:享受}')
    save = db.Column(db.Integer, doc='保存2个环境(30天){0或空:不享受,1:享受}')
    client = db.Column(db.Integer, doc='客户端{0或空:不享受,1:享受}')
    ssh = db.Column(db.Integer, doc='SSH直连{0或空:不享受,1:享受}')
    web_ide = db.Column(db.Integer, doc='WebIDE {0或空:不享受,1:享受}')
    discounts = db.Column(db.Integer, doc='训练营优惠{0或空:不享受,1:享受}')
    exempt_study = db.Column(db.Integer, doc='训练营课程免费学习{0或空:不享受,1:享受}')


class OtherUser(db.Model):
    __tablename__ = 'auth'
    # Auth_type = (('1', 'weibo'), ('2', 'weixin')) choices=Auth_type
    id = db.Column(db.Integer, primary_key=True)
    unid = db.Column(db.String(64))
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
    user = db.Column(db.Integer, db.ForeignKey('user.uid'), doc='发布人')
    desc = db.Column(db.String(256), doc='课程描述')
    img_path = db.Column(db.String(888), doc='封面')
    video = db.Column(db.String(888), doc='课程视频')
    course_type = db.Column(db.Integer, db.ForeignKey("course_type.id", ondelete="CASCADE"))
    status = db.Column(db.Integer, doc='状态', default=0)
    follower = db.Column(db.Integer, default=0, doc='关注人数')
    learner = db.Column(db.Integer, default=0, doc='学习人数')


class CourseTag(db.Model):
    """
    中间表  课程、标签的中间表
    """
    __tablename__ = 'course_tag'
    cid = db.Column(db.Integer, db.ForeignKey("course.id"), primary_key=True, doc='课程id')
    tid = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True, doc='标签id')
    is_delete = db.Column(db.Boolean, doc='状态(0存在对应关系;1不存在对应关系)')


class Section(db.Model):
    """
    章节表
    """
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), doc='章节名')
    video = db.Column(db.String(888), doc='章节视频')
    cid = db.Column(db.Integer, db.ForeignKey("course.id"))


class Comment(db.Model):
    """
    评论&回复表
    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, doc='评论或回复内容')
    uid = db.Column(db.Integer, doc='评论人或回复人')
    cid = db.Column(db.Integer, doc='课程id')
    sid = db.Column(db.Integer, doc='章节id')
    reply = db.Column(db.Integer, doc='自关联回复人')
    top = db.Column(db.Integer, doc='位置')
    excellent = db.Column(db.Integer, doc='精华(值大的是)')
    favorite = db.Column(db.Integer, doc='收藏总数')
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')


class Learn(db.Model):
    """
    学习状态表
    """
    __tablename__ = 'learning'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, doc='用户id')
    cid = db.Column(db.Integer, doc='课程id')
    sid = db.Column(db.Integer, doc='章节id')


class Goods(db.Model):
    """
    商品表
    """
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    good_type = db.Column(db.Integer, db.ForeignKey('course_type.id'))
    title = db.Column(db.String(24), doc='商品名称')
    price = db.Column(db.DECIMAL(20, 2), doc='商品价格')
    channel_type = db.Column(db.String(32), doc='普通/促销')
    period = db.Column(db.Integer, default=365, doc='有效期')
    is_launched = db.Column(db.Integer, default=0, doc='是否上架')


class Orders(db.Model):
    """
    订单表
    """
    __tablename__ = 'orders'
    order = db.Column(db.String(32), doc='订单号', primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.uid'))
    goods = db.Column(db.Integer, db.ForeignKey('goods.id'))
    trade_no = db.Column(db.String(32), doc='支付宝订单号')
    pay_time = db.Column(db.DateTime, default=datetime.now())
    pay_method = db.Column(db.String(32), doc='支付方式(微信/支付宝)')
    status = db.Column(db.String(32), doc='待支付/已支付/已取消')
    total = db.Column(db.DECIMAL(20, 2), doc='支付总金额')
    pay = db.Column(db.DECIMAL(20, 2), doc='实际支付金额')


class UserCourse(db.Model):
    """
    用户已购表
    """
    __tablename__ = 'user_course'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.uid'))
    course = db.Column(db.Integer, db.ForeignKey('course.id'))

# class QuestionType(db.Model):
#     """
#     帖子分类
#     """
#     __tablename__ = 'question_type'
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String(32), doc='帖子分类(实验评论,实验报告,实验问答)')


# class Question(db.Model):
#     """
#     帖子
#     """
#     __tablename__ = 'question'
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, doc='帖子内容')
#     type = db.Column(db.Integer,  doc='帖子类别id')
#     uid = db.Column(db.Integer, doc='发布人')
#     cid = db.Column(db.Integer, doc='课程id')
#     sid = db.Column(db.Integer, doc='章节id')
#     top = db.Column(db.Integer, doc='位置')
#     excellent = db.Column(db.Integer, doc='精品(值大的是)')
#     examine = db.Column(db.Integer, doc='查看总数')
#     favorite = db.Column(db.Integer, doc='收藏总数')
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
# class Favorite(db.Model):
#     """
#     点赞表
#     """
#     __tablename__ = 'favorite'
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.Integer, doc='点赞用户')
#     com_id = db.Column(db.Integer, doc='评论或回复id')
#     receive_id = db.Column(db.Integer, doc='收赞用户')
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
#
#
# class Report(db.Model):
#     """
#     报告表
#     """
#     __tablename__ = 'report'
#     id = db.Column(db.Integer, primary_key=True)
#     sid = db.Column(db.Integer, doc='所属章节')
#     uid = db.Column(db.Integer)
#     content = db.Column(db.Text, doc='报告内容')
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
#
#
# class Path(db.Model):
#     """
#     路径表
#     """
#     __tablename__ = 'path'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300), doc='路径名')
#     img = db.Column(db.String(900), doc='路径头图')
#     desc = db.Column(db.String(500), doc='路径简介')
#     section_sum = db.Column(db.Integr, doc='总章节数')
#     add_sum = db.Column(db.Integer, default=0, doc='添加人数')
#     study_time = db.Column(db.Integer, default=0, doc='预计学习时长（单位：分钟）')
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
#
#
# class Stage(db.Model):
#     """
#     路径阶段表
#     """
#     __tablename__ = 'stage'
#     id = db.Column(db.Integer, primary_key=True)
#     pid = db.Column(db.Integer, doc='路径id')
#     stage = db.Column(db.String(200), doc='阶段（如：第一阶段、第二阶段')
#     stage_name = db.Column(db.String(200), doc='阶段名（如：基础知识、编程语言）')
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
#
#
# class StageCourse(db.Model):
#     """
#     阶段课程表
#     """
#     __tablename__ = 'stage_course'
#     id = db.Column(db.Integer, primary_key=True)
#     stage_id = db.Column(db.Integer, doc='阶段id')
#     cid = db.Column(db.Integer, doc='课程id')
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
#
#
# class PathUser(db.Model):
#     """
#     路径收藏表
#     """
#     __tablename__ = 'path_user'
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.Integer)
#     create_time = db.Column(db.DateTime, default=datetime.now())
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
#
#
# class SecKill(db.Model):
#     """
#     秒杀活动表
#     """
#     __tablename__ = 'sec_kill'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), doc='标题')
#     start_time = db.Column(db.DateTime)
#     end_time = db.Column(db.DateTime)
#     img = db.Column(db.String(100))
#     is_delete = db.Column(db.Integer, default=0, doc='(0,未删除),(1,已经删除)逻辑删除')
#
#
# class SecCourse(db.Model):
#     """
#     秒杀-课程关系表
#     """
#     __tablename__ = 'sec_course'
#     id = db.Column(db.Integer, primary_key=True)
#     sid = db.Column(db.Integer)
#     cid = db.Column(db.Integer)
#
# # 优惠券表
# class Coupon(Base):
#     coupon = models.CharField(max_length=200)
#     uid = models.IntegerField()
#     price = models.IntegerField()
#     end_time = models.DateTimeField(null=True)
#     title = models.CharField(max_length=30, null=True)
#     img = models.CharField(max_length=200, default="coupon.jpg")
#
#     class Meta:
#         db_table = 'coupon'
#
#
# # 订单表
# class Order(Base):
#     uid = models.IntegerField()  # 购买用户
#     order = models.CharField(max_length=16)  # 订单号
#     price = models.IntegerField()  # 消费价格
#     behoof = models.CharField(max_length=200, null=True)  # 消费记录
#     is_succeed = models.IntegerField(default=0)  # 是否支付成功
#
#     class Meta:
#         db_table = "order"
#
#
# # 会员表
# class VIP(Base):
#     grade = models.CharField(max_length=20, null=True)  # 会员等级（普通会员、高级会员）
#     price = models.IntegerField(null=True)  # 会员价格（单位：分）
#     exempt_cour = models.IntegerField(null=True)  # 免费课程   {0或空:不享受,1:享受}
#     vip_cour = models.IntegerField(null=True)  # 会员课程   {0或空:不享受,1:享受}
#     environment = models.IntegerField(null=True)  # 实验环境联网   {0或空:不享受,1:享受}
#     save = models.IntegerField(null=True)  # 保存2个环境(30天)   {0或空:不享受,1:享受}
#     client = models.IntegerField(null=True)  # 客户端     {0或空:不享受,1:享受}
#     ssh = models.IntegerField(null=True)  # SSH直连   {0或空:不享受,1:享受}
#     webide = models.IntegerField(null=True)  # WebIDE    {0或空:不享受,1:享受}
#     discounts = models.IntegerField(null=True)  # 训练营优惠   {0或空:不享受,1:享受}
#     exempt_study = models.IntegerField(null=True)  # 训练营课程免费学习   {0或空:不享受,1:享受}
#
#     class Meta:
#         db_table = "vip"
#
#
# # 收藏表
# class Collection(Base):
#     uid = models.IntegerField()  # 用户id
#     iid = models.IntegerField()  # 帖子id
#
#     class Meta:
#         db_table = "collection"
#
#
# # 关注表
# class Follow(Base):
#     uid = models.IntegerField()  # 用户id
#     cid = models.IntegerField()  # 课程id
#
#     class Meta:
#         db_table = "follow"
#
#
# # 已学表
# class Learn(Base):
#     uid = models.IntegerField()  # 用户id
#     cid = models.IntegerField()  # 课程id
#     sid = models.IntegerField()  # 章节id
#
#     class Meta:
#         db_table = "learn"
#
#
# # 已购买表
# class Buy(Base):
#     uid = models.IntegerField()  # 用户id
#     cid = models.IntegerField()  # 课程id
#
