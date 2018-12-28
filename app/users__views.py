# !/usr/bin/env/python
# .*. encoding:utf-8 -*-
import os
import random
import re

from flask import Blueprint, url_for, render_template, request, jsonify, session, Config
from werkzeug.utils import redirect

from app.models import db, User
from utils.functions import is_login
from utils.settings import MEDIA_PATH

blue = Blueprint('user',__name__)



# 创建数据库
@blue.route('/create_db/',methods=['GET'])
def create_db():
    db.create_all()
    return 'done'


# 首页
@blue.route('/index/',methods=['GET'])
def index():
    return render_template('index.html')





# 注册
@blue.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        code = ''
        random_code = 'wertyuiopasdfghjklzxcvbnm123456789'
        for _ in range(4):
            code += random.choice(random_code)
        session['code'] = code
        return render_template('register.html',data=code)

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        imagecode = request.form.get('imagecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 验证参数
        if not all([mobile,imagecode,password,password2]):
            return jsonify({'code': 10001, 'msg': 'information is not all'})

        # 验证手机号
        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return jsonify({'code': 10002, 'msg': 'The phone number is incorrect.'})

        #  验证图片验证码
        if session.get('code') != imagecode:
            return jsonify({'code': 10003, 'msg': 'Image verification code is incorrect'})
        # 效验密码一致性
        if password != password2:
            return jsonify({'code': 10004, 'msg': 'Incorrect password'})

        # 效验用户是否已存在
        if  User.query.filter(User.phone == mobile).first():
            return jsonify({'code': 10005, 'msg': 'User already exists'})
        user = User()
        user.name = mobile
        user.password = password
        user.phone = mobile
        try:
            user.add_update()
            return jsonify({'code': 200, 'msg': 'registration success'})
        except:
            return jsonify({'code': 201, 'msg': 'registration failed'})




@blue.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')

        if not all([password,mobile]):
            return jsonify({'code': 10001, 'msg': 'information is not all'})

        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return jsonify({'code': 10002, 'msg': 'The phone number is incorrect.'})

        user = User.query.filter(User.phone == mobile).first()
        if user:
            if user.check_pwd(password):
                session['user_id'] = user.id
                return jsonify({'code': 200, 'msg': 'registration success'})

            else:
                return jsonify({'code': 10003, 'msg': 'Image verification code is incorrect'})

        else:
            return jsonify({'code': 10003, 'msg': 'User doesnt exits'})



@blue.route('/logout/', methods=['DELETE'])
@is_login
def user_logout():
    session.clear()
    return jsonify({'code':200})





@blue.route('/my/',methods=['GET'])
@is_login
def my():
    return render_template('my.html')

@blue.route('/my_info/',methods=['GET'])
def my_info():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict())


@blue.route('/profile/',methods=['GET','POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')

    if request.method == 'POST':
        name = request.form.get('name')
        avatar = request.files.get('avatar')
        if avatar:
            try:
                if not re.match('image/.*',avatar.mimetype):
                    return jsonify({'code': 10003, 'msg': 'The picture format is wrong'})
            except:
                return jsonify({'code': 10003, 'msg': 'The picture format is wrong'})
            user = User.query.get(session['user_id'])
            file_path = os.path.join(MEDIA_PATH, avatar.filename)
            # 保存头像到数据库
            user.avatar =  avatar.filename
            user.add_update()
            # 保存头像到本地
            avatar.save(file_path)
            return jsonify({'code':200,'avatar':avatar.filename})

        elif name:
            if User.query.filter_by(name=name).count():
                 return jsonify({'code':'10001','msg':'USER_IS_EXSITS'})
            else:
                user = User.query.get(session['user_id'])
                user.name = name
                user.add_update()
                return jsonify({'code':200,'msg':'success'})

        else:
            return jsonify({'code':'10009','msg':'errors'})



# 展示实名认证的界面
@blue.route('/auth/',methods=['GET','POST'])
@is_login
def auth():
    if request.method == 'GET':
        return render_template('auth.html')

# 实名认证
@blue.route('/auths/',methods=['GET','POST'])
@is_login
def auth_info():
    if request.method == 'GET':
        user_id =session['user_id']
        user = User.query.get(user_id)
        return jsonify(user.to_auth_dict())
    if request.method == 'POST':
        id_name = request.form.get('id_name')
        id_card = request.form.get('id_card')
        if not all([id_card,id_name]):
            return jsonify({'code':1000,'msg':'the msg is not all'})

        if not re.match(r'^[1-9]\d{17}$', id_card):
            return jsonify({'code':10000,'msg':'the id_card is error'})
        try:
            user = User.query.get(session['user_id'])
        except:
            return jsonify({'code': 10001, 'msg': 'the database is error'})
        try:
            user.id_card = id_card
            user.id_name = id_name
            user.add_update()
        except:
            return jsonify({'code': 10002, 'msg': 'the database is error'})
        return  jsonify({'code':200})