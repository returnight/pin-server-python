# -*- coding: utf-8 -*-
"""
    user.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints user

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

import ujson as json
from datetime import datetime
from mongoengine import Q

from flask import Blueprint
from flask import jsonify
from flask import g
from flask import make_response
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from pinserver.extensions import bcrypt
from pinserver.helpers import before_request

from pinserver.models.user import User
from pinserver.models.pin import Pin
from pinserver.models.timeline import Timeline

user = Blueprint('user', __name__)

user.before_request(before_request)

# support functions
def user_response(user):
    user_data = {
                'user_id':str(user.id),
                'email':user.email,
                'nickname':user.nickname,
                'avatar':user.avatar,
                }
    response = make_response(json.dumps(user_data), 200)
    response.headers['Version'] = '1'
    return response

@user.route('/reg', methods=['POST'])
def reg_user_post():
    """
        用户注册表单接收
        ~~~~~~~~~~~~~~~~

    """

    err_msg = None
    if not request.form['email']:
        return ('no email', 400)
    if not request.form['nickname']:
        return ('no nickname', 400)
    if not request.form['password']:
        return ('no password', 400)

    email = request.form['email']
    nickname = request.form['nickname']
    password = bcrypt.generate_password_hash(request.form['password'], 8)
    
    #avatar
    avatar = ''
    if 'avatar' in request.form:
        avatar = request.form['avatar']

    user = User(email=email,
                nickname=nickname,
                password=password,
                avatar=avatar,
                register_at=datetime.utcnow())

    user.save()
    
    user_id = str(user.id)
    
    session['user_id'] = user_id
    session.permanent = True
    
    user_data = {
                'user_id':user_id,
                'email':user.email,
                'nickname':user.nickname,
                'avatar':user.avatar,
                }
    response = make_response(json.dumps(user_data))
    #response.headers
    response.headers['Version'] = '1'
    return response

@user.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    user = User.objects(email=email).first()

    if not user:
        return ('email or password error', 401)

    if bcrypt.check_password_hash(user.password, request.form['password']):
        session['user_id'] = str(user.id)
        
        # 此参数当写入session时配置
        session.permanent = True
        return user_response(user)
    else:
        return ('email or password error', 401)

@user.route('/user', methods=['GET'])
def user_info():
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        user_id = str(user.id)
        user_data = {
                     'user_id':user_id,
                     'email':user.email,
                     'nickname':user.nickname,
                     'avatar':user.avatar,
                    }
        response = make_response(json.dumps(user_data))
        #response.headers
        response.headers['Version'] = '1'
        return response
    else:
        return ('session expired', 400)
        
@user.route('/user', methods=['POST'])
def user_info_post():
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        
        if request.form['nickname']:
            user.nickname = request.form['nickname']
            
        if request.form['avatar']:
            user.avatar = request.form['avatar']
        
        user.save()
        
        user_id = str(user.id)
        user_data = {
                     'user_id':user_id,
                     'email':user.email,
                     'nickname':user.nickname,
                     'avatar':user.avatar,
                    }
        response = make_response(json.dumps(user_data))
        #response.headers
        response.headers['Version'] = '1'
        return response
    else:
        return ('session expired', 400)
        
@user.route('/avatar/<email>')
def avata_url(email):
    if '@' not in email:
        return ('email error', 400)


    
    user = User.objects(email=email).first()

    res_data = {
                'avatar':user.avatar,
               }
    response = make_response(json.dumps(res_data))
    #response.headers
    response.headers['Version'] = '1'
    return response
        
@user.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('web_login'))

