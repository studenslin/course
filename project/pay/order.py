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


class VipList(Resource):
    """
    展示VIP列表
    """

    @login_required
    def get(self):
        vip_list = Vip.query.all()
        return marshal(vip_list, vip_fields)


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


path = os.path.join('../')
# app私钥
app_private_key_string = open(path + 'project/pay/private.text').read()
# 支付宝公钥
alipay_public_key_string = open(path + 'project/pay/public.text').read()


class Alipay(Resource):
    """
    沙箱支付
    """

    @login_required
    # 沙箱支付接口
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order')
        parser.add_argument('price')
        args = parser.parse_args()
        order = args.get('order')
        price = args.get('price')

        alipay = AliPay(
            appid="2016102400753303",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
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
        db.session.add(ords)
        db.session.commit()
        return {'code': 200, 'msg': 'ok'}


api.add_resource(VipList, '/vip_list')
api.add_resource(CreateOrder, '/create_order')
api.add_resource(Alipay, '/alipay')
