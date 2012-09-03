# -*- coding: utf-8 -*-
"""
    pin.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints pin

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

from flask import Blueprint
from flask import render_template
from flask import jsonify

from flask.views import MethodView

from pinserver.helpers import before_request
from pinserver.models.pin import Pin

pin = Blueprint('pin', pinserver)

pin.before_request(before_request)

#TODO
@pin.route('/pin')
def show_pin():
	if g.user_id:
		return jsonify(user_id=g.user_id)


