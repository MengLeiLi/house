# !/usr/bin/env/python
# .*. encoding:utf-8 -*-
import datetime
import os

from flask import Blueprint, url_for, render_template, request, jsonify, session, Config

from app.models import User, House, Area, Facility, HouseImage, Order
from utils.functions import is_login
from utils.settings import MEDIA_PATH

blue_house =Blueprint('house',__name__)

@blue_house.route('/my_house/',methods=['GET'])
@is_login
def my_house():

    return  render_template('myhouse.html')


@blue_house.route('/my_auth/',methods=['GET'])
def my_auth():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user.id_name:
        # 已经完成实名认证，查询当前用户的房屋信息
        house_list = House.query.filter(House.user_id == user_id).order_by(House.id.desc())
        house_list2 = []
        for house in house_list:
            house_list2.append(house.to_dict())
        return jsonify(code='200', house_info=house_list2)
    else:
        # 没有完成实名认证
        return jsonify(code='123')



@blue_house.route('/detail/',methods=['GET'])
@is_login
def detail():
    return render_template('detail.html')

@blue_house.route('/detail/<int:id>/',methods=['GET'])
def house_detail(id):
    # 查询房屋信息
    house = House.query.get(id)
    # 查询设施信息
    facility_list = house.facilities
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    # 判断房屋信息是否为当前登录的用户发布,如果不是则显示预定按钮
    booking = 1
    if 'user_id' in session:
        if house.user_id == session['user_id']:
            booking = 0
    return jsonify(code=200,house=house.to_full_dict(),facility_list=facility_dict_list,booking=booking)


# 查询数据库中关于房屋设施及所处地区的数据
@blue_house.route('/area_facility/',methods=['GET'])
def area_facility():
    # 查询地址
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    # 查询设施
    facility_list = Facility.query.all()
    facility_dict_list = [ facility.to_dict() for facility in facility_list]
    return jsonify(area=area_dict_list,facility=facility_dict_list)



@blue_house.route('/new_house/',methods=['GET','POST'])
@is_login
def new_house():
    if request.method == 'GET':
        return  render_template('newhouse.html')
    if request.method == 'POST':
        params = request.form.to_dict()
        facility_ids = request.form.getlist('facility')
        # 创建用户信息
        house = House()
        house.user_id = session['user_id']
        house.area_id = params.get('area_id')
        house.title = params.get('title')
        house.price = params.get('price')
        house.address = params.get('address')
        house.room_count = params.get('room_count')
        house.acreage = params.get('acreage')
        house.beds = params.get('beds')
        house.unit = params.get('unit')
        house.capacity = params.get('capacity')
        house.deposit = params.get('deposit')
        house.min_days = params.get('min_days')
        house.max_days = params.get('max_days')

        # 根据设备的编号查询设备对象
        if facility_ids:
            facility=Facility.query.filter(Facility.id.in_(facility_ids)).all()
            house.facilities = facility
        house.add_update()
        return jsonify(code=200,house_id=house.id)


@blue_house.route('/image_house/',methods=['POST'])
def image_house():
    if request.method == 'POST':

        house_id = request.form.get('house_id')
        f1 = request.files.get('house_image')
        # 保存在本地
        file_path =os.path.join(MEDIA_PATH,f1.filename)
        f1.save(file_path)

        # 增加house_image表的数据
        image=HouseImage()
        image.house_id = house_id
        image.url = f1.filename
        image.add_update()

        # 增加house表的图片
        house =House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url =f1.filename
            house.add_update()
        return jsonify(code=200,url=file_path,f1_filename=f1.filename)



@blue_house.route('/index/',methods=['GET'])
def index():
    return render_template('index.html')



@blue_house.route('/hindex/', methods=['GET'])
def house_index():
    # 返回最新的5个房屋信息
    hlist = House.query.order_by(House.id.desc()).all()[:5]
    hlist2 = [house.to_dict() for house in hlist]
    # 查找地区信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        user_name = user.name
        code = 200
        return jsonify(code=code, name=user_name, hlist=hlist2, alist=area_dict_list)
    return jsonify(hlist=hlist2, alist=area_dict_list)


@blue_house.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')





@blue_house.route('/my_search/', methods=['GET'])
def my_search():
    # 先获取区域id，订单开始时间，结束时间
    aid = request.args.get('aid')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')
    # 获取某个区域的房屋信息
    houses = House.query.filter(House.area_id == aid)
    # 订单的三种情况，查询出的房屋都不能展示
    order1 = Order.query.filter(Order.end_date >= ed, Order.begin_date <= ed)
    order2 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= sd)
    order3 = Order.query.filter(Order.begin_date >= sd, Order.end_date <= ed)
    house1 = [order.house_id for order in order1]
    house2 = [order.house_id for order in order2]
    house3 = [order.house_id for order in order3]
    # 去重
    not_show_house_id = list(set(house1 + house2 + house3))
    # 最终展示的房屋信息
    houses = houses.filter(House.id.notin_(not_show_house_id))
    # 排序
    if sk == 'new':
        houses = houses.order_by('-id')
    elif sk == 'booking':
        houses = houses.order_by('-order_count')
    elif sk == 'price-inc':
        houses = houses.order_by('price')
    elif sk == 'price-des':
        houses = houses.order_by('-price')

    house_info = [house.to_dict() for house in houses]
    return jsonify(code=200, house_info=house_info)