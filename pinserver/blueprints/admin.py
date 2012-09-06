# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints admin

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

from functools import wraps

from flask import request
from flask import Response
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import render_template

admin = Blueprint('admin', __name__)

def check_basic_auth(username, password):
    return username == 'swipppe' and password == 'admin'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_basic_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@admin.before_request
def admin_before_request():
    g.admin = None
    if 'admin' in session:
        g.admin = session['admin']

@admin.route('/admin/login')
@requires_basic_auth
def admin_login():
    session['admin'] = 'admin'
    return redirect(url_for('admin.admin_index'))

# only for test
@admin.route('/admin/')
def admin_index():
    if g.admin:
        return render_template('admin/index.html')
    return redirect(url_for('admin.admin_login'))

@admin.route('/admin/user/', defaults={'page':1})
@admin.route('/admin/user/page/<int:page>')
def admin_user(page):
    pass

    

    