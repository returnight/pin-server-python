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
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from flask.views import MethodView

from pinserver.helpers import before_request
from pinserver.models.user import User
from pinserver.models.pin import Pin
from pinserver.models.timeline import Timeline

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

        timeline = Timeline(pin=pin,
                            owner=owner)
        timeline.save()

        res_data = {
            'pin_id':str(pin.id),
            'content':pin.content,
            'create_at':pin.create_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
        }
        response = make_response(json.dumps(res_data))
        #response.headers
        #response.headers['Version'] = '1'
        return response
    else:
        err_msg = 'session timeout'
        return jsonify(err_msg=err_msg)

@pin.route('/del_pin/<pin_id>')
def del_pin(pin_id):
    if len(pin_id) == 24:
        pin = Pin.objects(id=pin_id).first()
        if pin:
            pin.delete()
            return jsonify(status='delete success')
        return jsonify(err_msg='no this pin')
    return jsonify(err_msg='need pin_id')

@pin.route('/pins')
def show_pins():
    if g.user_id:
        pins = Pin.objects(owner=g.user_id)[:5].order_by('-create_at')
        pin_list = []
        for pin in pins:
            pin_item = {}
            pin_item['pin_id'] = str(pin.id)
            pin_item['content'] = pin.content
            pin_item['create_at'] = pin.create_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            pin_list.append(pin_item)
        res_data = {
            'total':len(pin_list),
            'items':pin_list,
        }
        response = make_response(json.dumps(res_data))
        return response
    return ('show_pins session timeout', 400)

@pin.route('/pins/before/<pin_id>')
def show_pins_before(pin_id):
    if g.user_id:
        pins = Pin.objects(__raw__={'_id':{"$lt":pin_id}, 'owner':g.user_id})[:5].order_by('-create_at')
        pin_list = []
        for pin in pins:
            pin_item = {}
            pin_item['pin_id'] = str(pin.id)
            pin_item['content'] = pin.content
            pin_item['create_at'] = pin.create_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            pin_list.append(pin_item)
        res_data = {
            'total':len(pin_list),
            'items':pin_list,
        }
        response = make_response(json.dumps(res_data))
        return response
    return ('show_pins_before session timeout', 400)

@pin.route('/web/pin')
def web_pin():
    if g.user_id:
        return """
        <!doctype html>
        <title>发布Pin</title>
        <h1>发布Pin</h1>
        <form action="/pin" method=post>
          <p><input type=text name=content>
             <input type=submit value="发布">
        </form>    
        """
    return redirect(url_for('web_login'))







