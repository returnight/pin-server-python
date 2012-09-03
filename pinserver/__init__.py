# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~
    
    Pinserver Main

    先不用急着拆分逻辑

    导入顺序
    --------

        #. 导入标准库

        #. 导入所需第三方库

        #. 导入flask库

        #. 导入flask ext库

        #. 导入项目辅助工具

        #. 导入项目包（model、view）

    函数顺序
    --------

        #. 辅助函数

        #. before_request

        #. teardown_request

        #. 各种路由

        #. GET POST要分开写

    依赖库
    --------
    bcrypt需要gcc和python-dev
    psycopg2需要libpq-dev

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
    
    Session
    ---------
    
    # 此参数当写入session时配置
    session.permanent = True

"""

import os
import ujson as json
from datetime import datetime

from flask import Flask
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import render_template
from flask import make_response

from flask.ext.bcrypt import Bcrypt
from flask.ext.mongoengine import MongoEngine


from pinserver.config import DefaultConfig
#from pinserver.models.user import User

# 建立应用
app = Flask(__name__)


# 导入配置
# 从对象导入
app.config.from_object(DefaultConfig())
# 从配置文件导入配置
#app.config.from_pyfile('config.cfg')
# 由环境变量指定配置文件位置并导入
# 首先要配置环境变量
# $ export PIN_SERVER_SETTINGS=/path/to/config_file
app.config.from_envvar('PIN_SERVER_SETTINGS', silent=True)

# 初始化 Bcrypt
bcrypt = Bcrypt(app)

# 初始化 Mongodb
db = MongoEngine(app)

from pinserver.models.user import User
#from pinserver.models.pin import Pin

# helper functions
@app.template_filter('user_datetime')
def user_datetime(datetime):
    return datetime.strftime('%Y-%m-%d @ %H:%M')


def err_response(err_msg):
    res_body = {'err_msg':err_msg}
    response = make_response(json.dumps(res_body), 400)
    return response

def user_response(user):
    user_data = {
                'user_id':str(user.id),
                'email':user.email,
                'nickname':user.nickname,
                }
    response = make_response(json.dumps(user_data), 200)
    response.headers['Version'] = '1'
    return response


# routes
@app.before_request
def before_request():
    """
    每次请求前从session中提出用户信息
    """
    g.user_id = None
    if 'user_id' in session:
        g.user_id = session['user_id']
    
    #TODO
    # 当没有session的时候处理
    # else:
    
    
        # 不必在这里取出用户信息，徒增负担
        #g.user = User.objects(id=user_id).first()


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/reg', methods=['POST'])
def reg_user_post():
    """
        用户注册表单接收
        ~~~~~~~~~~~~~~~~

    """

    err_msg = None
    if not request.form['email']:
        err_msg = 'no email'
        return err_response(err_msg)
    if not request.form['nickname']:
        err_msg = 'no nickname'
        return err_response(err_msg)
    if not request.form['password']:
        err_msg = 'no password'
        return err_response(err_msg)

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
                avatar=avatar)

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

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    user = User.objects(email=email).first()

    if not user:
        err_msg = 'email or password error'
        return err_response(err_msg)

    if bcrypt.check_password_hash(user.password, request.form['password']):
        session['user_id'] = str(user.id)
        
        # 此参数当写入session时配置
        session.permanent = True
        return user_response(user)
    else:
        err_msg = 'email or password error'
        return err_response(err_msg)

@app.route('/user_info')
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
        err_msg = 'session expired'
        return err_response(err_msg)
        
@app.route('/user_info', methods=['POST'])
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
        err_msg = 'session expired'
        return err_response(err_msg)
        
@app.route('/avatar/<email>')
def avata_url(email):
    if '@' not in email:
        err_msg = 'email error'
        return err_response(err_msg)
    
    user = User.objects(email=email).first()

    res_data = {
                'avatar':user.avatar,
               }
    response = make_response(json.dumps(res_data))
    #response.headers
    response.headers['Version'] = '1'
    return response
        
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('web_login'))

@app.route('/upload', methods=['POST'])
def upload_post():
    file = request.files['file']
    if file:
        # TODO filename should be fixed
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = app.config['FILE_URL'] % filename
        response_data = {'file_url':file_url}
        response = make_response(json.dumps(response_data))
        response.headers['Version'] = '1'
        return response
        
@app.route('/upload_avatar', methods=['POST'])
def upload_avatar_post():
    file = request.files['file']
    if file:
        # TODO filename should be fixed
        filename = file.filename
        file.save(os.path.join(app.config['AVATAR_UPLOAD_FOLDER'], filename))
        file_url = app.config['AVATAR_URL'] % filename
        response_data = {'avatar':file_url}
        response = make_response(json.dumps(response_data))
        response.headers['Version'] = '1'
        return response

# for web test    
@app.route('/web/reg', methods=['GET'])
def web_reg_user():
    """
        用户注册 Web 界面
        ~~~~~~~~~~~~~~~~~

    """
    if g.user_id:
        return redirect(url_for('web_info'))

    return render_template('reg.html')

@app.route('/web/login', methods=['GET'])
def web_login():
    if g.user_id:
        return redirect(url_for('web_info'))
        
    return render_template('login.html')

@app.route('/web/info')
def web_info():
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        return render_template('info.html', user=user)
    return redirect(url_for('web_login'))
    
@app.route('/web/set_info')
def web_set_info():
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        return render_template('set_info.html', user=user)
    return redirect(url_for('web_login'))

@app.route('/web/upload')
def web_upload():
    return '''
    <!doctype html>
    <title>文件上传</title>
    <h1>文件上传</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/web/upload_avatar')
def web_upload_avatar():
    return '''
    <!doctype html>
    <title>头像上传</title>
    <h1>头像上传</h1>
    <form action="/upload_avatar" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

from pinserver.blueprints.pin import pin
app.register_blueprint(pin)
from pinserver.blueprints.timeline import timeline
app.register_blueprint(timeline)