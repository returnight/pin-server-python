# -*- coding: utf-8 -*-
"""
    upload.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints upload

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

import os

from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import current_app

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_post():
    file = request.files['file']
    if file:
        # TODO filename should be fixed
        filename = file.filename
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        file_url = current_app.config['FILE_URL'] % filename
        response_data = {'file_url':file_url}
        response = make_response(json.dumps(response_data))
        response.headers['Version'] = '1'
        return response

@upload.route('/upload_avatar', methods=['POST'])
def upload_avatar_post():
    file = request.files['file']
    if file:
        # TODO filename should be fixed
        filename = file.filename
        file.save(os.path.join(current_app.config['AVATAR_UPLOAD_FOLDER'], filename))
        file_url = current_app.config['AVATAR_URL'] % filename
        response_data = {'avatar':file_url}
        response = make_response(json.dumps(response_data))
        response.headers['Version'] = '1'
        return response

