# -*- codeing = utf-8 -*-
# @Time : 2022/4/7 15:06
# @Author : linyaxuan
# @File : order.py
# @Software : PyCharm
import datetime
import os.path
import random
from alipay import AliPay
from flask import Blueprint, g
from flask_restful import Resource, reqparse, Api, marshal
from common.models.model import Vip, Orders

from common.utils.login_utils import login_required
from common.models import rds, db
from common.model_fields.user_fields import vip_fields
from common.utils.custom_output_json import custom_output_json

order_bp = Blueprint('order_bp', __name__)
api = Api(order_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


path = os.path.join('../')
# app私钥
app_private_key_string = open(path + 'project/pay/private.text').read()
# 支付宝公钥
alipay_public_key_string = open(path + 'project/pay/public.text').read()


class VipList(Resource):
    """
    展示VIP列表
    """

    @login_required
    def get(self):
        vip_list = Vip.query.all()
        return marshal(vip_list, vip_fields)


class AlipayBack(Resource):
    """
    支付回调
    """

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid')
        parser.add_argument('order')
        args = parser.parse_args()
        order = args.get('order')
        cid = args.get('cid')
        uid = g.user_id
        # 判断订单是否已存在,或已完成支付
        orders = Orders.query.filter_by(order=order, user=uid).first()
        if not orders or orders.status == 1:
            return {'code': 405, 'msg': 'Order already exists or payment has been completed'}
        alipay = AliPay(
            appid='',
            # 默认回调地址
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        # 支付宝查询交易
        response = alipay.api_alipay_trade_query(order)
        if response.get("code") != "10000" or response.get("trade_status") != "TRADE_SUCCESS":
            return {"code": 405, "message": "开通失败"}
        # 支付成功，修改支付状态
        orders.status = str(1)
        db.session.commit()
        # TODO
        """
        1. 获取用户开通的会员信息
        2. 修改用户的会员信息
        """


class CreateOrder(Resource):
    """
    生成订单
    """

    @login_required
    def get(self):
        uid = g.user_id
        order = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uid) + str(random.randint(1000, 9999)))
        rds.setex('order_{}'.format(uid), 60 * 5, order)
        return {'code': 200, 'order': order}


class Alipay(Resource):
    """
    沙箱支付
    """

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order')
        parser.add_argument('price')
        args = parser.parse_args()
        order = args.get('order')
        price = args.get('price')
        uid = g.user_id
        #  判断订单是否存在（是否购买）
        order_lis = Orders.query.filter_by(order=order, user=uid).first()
        if order_lis or order_lis.status == 1:
            return {'code': 400, 'msg': 'This order already exists'}
        alipay = AliPay(
            appid="2016102400753303",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 调用支付接口，生成支付链接
        # 电脑网站支付，需要跳转到
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order,  # 订单id，应该从前端获取
            total_amount=price,  # 订单总金额
            subject="阿里云付款",  # 付款标题信息
            return_url="http:127.0.0.1:8080/alipay",  # 付款成功回调地址(可以为空)
            notify_url=None  # 付款成功后异步通知地址（可以为空）
        )
        # 将这个url复制到浏览器，就会打开支付宝支付页面
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        print(pay_url)
        return {'code': 200, 'data': pay_url}

    # 订单入库
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order')
        parser.add_argument('price')
        parser.add_argument('record')
        args = parser.parse_args()
        order = args.get('order')
        price = args.get('price')
        record = args.get('record')
        uid = g.user_id
        print('sss', record)

        orders = rds.get('order_{}'.format(uid))
        orders = orders.decode()
        if order != orders:
            return {'code': 400, 'msg': 'Parameter error'}
        ords = Orders()
        ords.user = uid
        ords.order = order
        ords.pay = price
        ords.total = price
        ords.record = record
        db.session.add(ords)
        db.session.commit()
        return {'code': 200, 'msg': 'ok'}


class VerifyOrder(Resource):
    """
    检验订单信息
    """

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order')
        args = parser.parse_args()
        order = args.get('order')
        uid = g.user_id
        print(order, uid)
        order = Orders.query.filter_by(order=order, user=uid).first()
        print('1111', order)
        # if not order or order.status != 0:
        if order:
            return {'code': 200, 'msg': 'pay success'}
        return {'code': 500, 'msg': 'Payment of this order has been completed'}


api.add_resource(VipList, '/vip_list')
api.add_resource(CreateOrder, '/create_order')
api.add_resource(Alipay, '/alipay')
api.add_resource(VerifyOrder, '/ver_alipy')
