# -*- coding: utf-8 -*-
"""
    pin.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints pin

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

from pinserver.helpers import before_request
from pinserver.models.user import User
from pinserver.models.pin import Pin
from pinserver.models.timeline import Timeline

pin = Blueprint('pin', __name__)

pin.before_request(before_request)

#support functions
def pins_pack(pins):
    pin_list = []
    for pin in pins:
        pin_item = {}
        pin_item['pin_id'] = str(pin.id)
        pin_item['content'] = pin.content
        pin_item['avatar'] = pin.avatar
        pin_item['create_at'] = pin.create_at.strftime('%Y-%m-%d %H:%M:%S')
        pin_list.append(pin_item)
    res_data = {
        'total':len(pin_list),
        'items':pin_list,
    }
    return res_data

@pin.route('/pin', methods=['POST'])
def pin_post():
    if g.user_id:
        content = request.form['content']
        owner = User.objects(id=g.user_id).first()
        pin = Pin(content=content,
                  owner=owner,
                  create_at=datetime.utcnow(),
                  avatar=owner.avatar)
        pin.save()

        timeline = Timeline(pin=pin,
                            owner=owner,
                            create_at=datetime.utcnow())
        timeline.save()

        owner.update(inc__pins_count=1)

        res_data = {
            'pin_id':str(pin.id),
            'content':pin.content,
            'avatar':pin.avatar,
            'create_at':pin.create_at.strftime('%Y-%m-%d %H:%M:%S'),
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
    if g.user_id:
        if len(pin_id) == 24:
            pin = Pin.objects(id=pin_id).first()
            if pin:
                pin.delete()

                # delete pin from timeline
                timelines = Timeline.objects(pin=pin_id)
                for timeline in timelines:
                    timeline.delete()
                      
                return jsonify(status='delete success')
            return jsonify(err_msg='no this pin')
        return jsonify(err_msg='need pin_id')
    return ('del pin session timeout', 400)

@pin.route('/pins')
def show_pins():
    if g.user_id:
        pins = Pin.objects(owner=g.user_id)[:5].order_by('-create_at')
        res_data = pins_pack(pins)
        response = make_response(json.dumps(res_data))
        return response
    return ('show_pins session timeout', 400)

@pin.route('/pins/before/<pin_id>')
def show_pins_before(pin_id):
    if g.user_id:
        time_tag = Pin.objects(id=pin_id).first().create_at
        pins = Pin.objects(Q(create_at__lt=time_tag)&Q(owner=g.user_id))[:5].order_by('-create_at')
        res_data = pins_pack(pins)
        response = make_response(json.dumps(res_data))
        return response
    return ('show_pins_before session timeout', 400)

@pin.route('/pins/user/<user_id>')
def show_pins_user(user_id):
    if g.user_id:
        pins = Pin.objects(owner=user_id)[:5].order_by('-create_at')
        res_data = pins_pack(pins)
        response = make_response(json.dumps(res_data))
        return response
    return ('show_pins session timeout', 400)

@pin.route('/pins/user/<user_id>/before/<pin_id>')
def show_pins_user_before(user_id, pin_id):
    if g.user_id:
        time_tag = Pin.objects(id=pin_id).first().create_at
        pins = Pin.objects(Q(create_at__lt=time_tag)&Q(owner=user_id))[:5].order_by('-create_at')
        res_data = pins_pack(pins)
        response = make_response(json.dumps(res_data))
        return response
    return ('show_pins_before session timeout', 400)

# like
@pin.route('/like/<pin_id>')
def like_pin(pin_id):
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        pin = Pin.objects(id=pin_id, likes__nin=[user]).first()
        if pin:
            pin.update(push__likes=user, inc__likes_count=1)
            return ('like success', 200)
        return ('already liked', 400)
    return ('like pin session timeout', 400)

@pin.route('/unlike/<pin_id>')
def unlike_pin(pin_id):
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        pin = Pin.objects(id=pin_id).first()
        pin.update(pull__likes=user, inc__likes_count=-1)
        return ('unlike success', 200)
    return ('unlike pin session timeout', 400)

@pin.route('/pin/<pin_id>/likes', defaults={'page_num':1})
@pin.route('/pin/<pin_id>/likes/page/<int:page_num>')
def pin_likes(pin_id, page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        pin = Pin.objects(id=pin_id).fields(slice__likes=[offset, limit]).first()

        like_list = []
        for like in pin.likes:
            like_item = {}
            like_item['user_id'] = str(like.id)
            like_item['avatar'] = like.avatar
            like_list.append(like_item)
        res_data = {
            'total':len(like_list),
            'items':like_list,
        }
        return (json.dumps(res_data), 200)
    return ('likes list session timeout', 400)


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







