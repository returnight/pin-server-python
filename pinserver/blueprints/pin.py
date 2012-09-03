# -*- coding: utf-8 -*-
"""
    pin.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints pin

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

import ujson as json

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import g
from flask import make_response

from flask.views import MethodView

from pinserver.helpers import before_request
from pinserver.models.user import User
from pinserver.models.pin import Pin

pin = Blueprint('pin', __name__)

pin.before_request(before_request)

@pin.route('/pin', methods=['POST'])
def pin_post():
	if g.user_id:
		content = request.form['content']
		owner = User.objects(id=g.user_id).first()
		pin = Pin(content=content,
				  owner=owner)
		pin.save()

		res_data = {
					'pin_id':str(pin.id),
					'content':pin.content,
					'create_at':pin.create_at.strftime('%Y-%m-%d %H:%M:%S'),
					}
		response = make_response(json.dumps(user_data))
	    #response.headers
	    response.headers['Version'] = '1'
	    return response
	else:
		err_msg = 'session timeout'
		return jsonify(err_msg=err_msg)

@pin.route('/pins')
def show_pins():
	if g.user_id:
		return jsonify(user_id=g.user_id)

@pin.route('/web/pin')
def web_pin():
	if g.user_id:
		return """
		<!doctype html>
	    <title>发布Pin</title>
	    <h1>发布Pin</h1>
	    <form action="/pin" method=post>
	      <p><input type=text name=contect>
	         <input type=submit value="发布g>
	    </form>	
		"""
	return redirect(url_for('web_login'))







