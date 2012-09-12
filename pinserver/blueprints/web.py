# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints admin

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

from flask import request
from flask import Response
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import render_template

from pinserver.models.user import User

web = Blueprint('web', __name__)

# for web test    
@web.route('/web/reg', methods=['GET'])
def web_reg_user():
    """
        用户注册 Web 界面
        ~~~~~~~~~~~~~~~~~

    """
    if g.user_id:
        return redirect(url_for('.web_info'))

    return render_template('reg.html')

@web.route('/web/login', methods=['GET'])
def web_login():
    if g.user_id:
        return redirect(url_for('.web_info'))
        
    return render_template('login.html')

@web.route('/web/info')
def web_info():
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        return render_template('info.html', user=user)
    return redirect(url_for('.web_login'))
    
@web.route('/web/set_info')
def web_set_info():
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        return render_template('set_info.html', user=user)
    return redirect(url_for('.web_login'))

@web.route('/web/upload')
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

@web.route('/web/upload_avatar')
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
