# !/usr/bin/env/python
# .*. encoding:utf-8 -*-
from datetime import datetime

from flask import Blueprint, render_template, request, session, jsonify

from app.models import House, Order
from utils.functions import is_login

blue_order =Blueprint('order',__name__)

@blue_order.route('/booking/',methods=['GET'])
def booking():

    return render_template('booking.html')


@blue_order.route('/order_id/',methods=['POST'])
def order_id():
    # 创建订单模型
    # 1. 获得开始时间和结束时间
    begin_date = datetime.strptime(request.form.get('begin_date'),'%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'),'%Y-%m-%d')

    # 2. 获得用户和房屋id
    user_id = session['user_id']
    house_id = request.form.get('house_id')

    # 获得房屋对象
    house = House.query.get(house_id)
    oreder = Order()
    oreder.user_id = user_id
    oreder.house_id = house_id
    oreder.begin_date = begin_date
    oreder.end_date =end_date
    oreder.days =(end_date-begin_date).days + 1
    oreder.amount = oreder.days * house.price
    oreder.house_price =house.price
    oreder.add_update()
    return jsonify(code=200)

@blue_order.route('/orders/',methods=['GET'])
def orders():
    return render_template('orders.html')

@blue_order.route('/all_order/', methods=['GET'])
def all_order():
    uid = session['user_id']
    order_list = Order.query.filter(Order.user_id == uid).order_by(Order.id.desc())
    order_list2 = [order.to_dict() for order in order_list]
    return jsonify(olist=order_list2)





@blue_order.route('/lorders/',methods=['GET'])
def lorders():
    return render_template('lorders.html')


@blue_order.route('/fd/',methods=['GET'])
def find_orders():
    uid=session['user_id']
    #查询当前用户的所有房屋编号
    hlist=House.query.filter(House.user_id==uid)
    hid_list=[house.id for house in hlist]
    #根据房屋编号查找订单
    order_list=Order.query.filter(Order.house_id.in_(hid_list)).order_by(Order.id.desc())
    #构造结果
    olist=[order.to_dict() for order in order_list]
    return jsonify(olist=olist)







@blue_order.route('/lorders/<int:id>/',methods=['PUT'])
def status(id):
    #接收参数：状态
    status=request.form.get('status')
    #查找订单对象
    order=Order.query.get(id)
    #修改
    order.status=status
    #如果是拒单，需要添加原因
    if status=='REJECTED':
        order.comment=request.form.get('comment')
    #保存
    try:
        order.add_update()
    except:
        return jsonify(code=1001)

    return jsonify(code=200)