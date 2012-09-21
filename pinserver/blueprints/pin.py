# -*- coding: utf-8 -*-
"""
    pin.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints pin

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

import ujson as json
#import json
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
from pinserver.models.comment import Comment

pin = Blueprint('pin', __name__)

pin.before_request(before_request)

#support functions
def pins_pack(pins, user):
    pin_list = []
    for pin in pins:
        pin_item = {}
        pin_item['pin_id'] = str(pin.id)
        pin_item['type'] = pin.type
        pin_item['content'] = pin.content
        pin_item['pic'] = pin.pic
        pin_item['avatar'] = pin.avatar
        pin_item['comments_count'] = pin.comments_count
        pin_item['isliked'] = 1 if user in pin.likes else 0

        if pin.comments_count == 0:
            pin_item['comments'] = []
        elif pin.comments_count == 1:
            first_comment = {
                'content':pin.first_comment,
                'author_id':str(pin.first_comment_user.id),
                'nickname':pin.first_comment_user.nickname,
                'avatar':pin.first_comment_user.avatar,
                'create_at':pin.first_comment_create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            pin_item['comments'] = [first_comment]
        elif pin.comments_count >= 2:
            first_comment = {
                'content':pin.first_comment,
                'author_id':str(pin.first_comment_user.id),
                'nickname':pin.first_comment_user.nickname,
                'avatar':pin.first_comment_user.avatar,
                'create_at':pin.first_comment_create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            last_comment = {
                'content':pin.last_comment,
                'author_id':str(pin.last_comment_user.id),
                'nickname':pin.last_comment_user.nickname,
                'avatar':pin.last_comment_user.avatar,
                'create_at':pin.last_comment_create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            pin_item['comments'] = [first_comment, last_comment]


        pin_item['likes_count'] = pin.likes_count
        pin_item['create_at'] = pin.create_at.strftime('%Y-%m-%d %H:%M:%S')
        pin_list.append(pin_item)
    res_data = {
        'total':len(pin_list),
        'items':pin_list,
    }
    return res_data

# droped
# def pins_isliked_pack(pins, user):
#     pin_list = []
#     for pin in pins:
#         pin_item = {}
#         pin_item['isliked'] = 1 if user in pin.likes else 0
#         pin_item['pin_id'] = str(pin.id)
#         pin_item['type'] = pin.type
#         pin_item['content'] = pin.content
#         pin_item['pic'] = pin.pic
#         pin_item['avatar'] = pin.avatar
#         pin_item['create_at'] = pin.create_at.strftime('%Y-%m-%d %H:%M:%S')
#         pin_list.append(pin_item)
#     res_data = {
#         'total':len(pin_list),
#         'items':pin_list,
#     }
#     return res_data

@pin.route('/pin', methods=['POST'])
def pin_post():
    if g.user_id:

        pin_type = 1
        if 'type' in request.form:
            pin_type = int(request.form['type'])

        content = ''
        if 'content' in request.form:
            content = request.form['content']

        pic = ''
        if 'pic' in request.form:
            pic = request.form['pic']

        owner = User.objects(id=g.user_id).first()
        pin = Pin(type=pin_type,
                  content=content,
                  pic=pic,
                  owner=owner,
                  create_at=datetime.utcnow(),
                  avatar=owner.avatar)
        pin.save()

        timeline = Timeline(pin=pin,
                            owner=owner,
                            create_at=datetime.utcnow())
        timeline.save()

        if owner.fans:
            for fan in owner.fans:
                fan_timeline = Timeline(pin=pin,
                                        owner=fan,
                                        create_at=datetime.utcnow())
                fan_timeline.save()

        owner.update(inc__pins_count=1)

        res_data = {
            'pin_id':str(pin.id),
            'type':pin.type,
            'content':pin.content,
            'avatar':pin.avatar,
            'owner_id':str(pin.owner.id),
            'create_at':pin.create_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        response = make_response(json.dumps(res_data))
        #response.headers
        #response.headers['Version'] = '1'
        return response
    else:
        return ('pin post session timeout', 400)

@pin.route('/pin/<pin_id>', methods=['GET'])
def pin_detail(pin_id):
    if g.user_id:
        pin = Pin.objects(id=pin_id).first()

        user = User.objects(id=g.user_id).first()
        isliked = 1 if user in pin.likes else 0

        pin_item = {}
        pin_item['pin_id'] = str(pin.id)
        pin_item['type'] = pin.type
        pin_item['content'] = pin.content
        pin_item['pic'] = pin.pic
        pin_item['avatar'] = pin.avatar
        pin_item['comments_count'] = pin.comments_count
        pin_item['isliked'] = 1 if user in pin.likes else 0

        if pin.comments_count == 0:
            pin_item['comments'] = []
        elif pin.comments_count == 1:
            first_comment = {
                'content':pin.first_comment,
                'author_id':str(pin.first_comment_user.id),
                'nickname':pin.first_comment_user.nickname,
                'avatar':pin.first_comment_user.avatar,
                'create_at':pin.first_comment_create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            pin_item['comments'] = [first_comment]
        elif pin.comments_count >= 2:
            first_comment = {
                'content':pin.first_comment,
                'author_id':str(pin.first_comment_user.id),
                'nickname':pin.first_comment_user.nickname,
                'avatar':pin.first_comment_user.avatar,
                'create_at':pin.first_comment_create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            last_comment = {
                'content':pin.last_comment,
                'author_id':str(pin.last_comment_user.id),
                'nickname':pin.last_comment_user.nickname,
                'avatar':pin.last_comment_user.avatar,
                'create_at':pin.last_comment_create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            pin_item['comments'] = [first_comment, last_comment]


        pin_item['likes_count'] = pin.likes_count
        pin_item['create_at'] = pin.create_at.strftime('%Y-%m-%d %H:%M:%S')


        return (json.dumps(pin_item), 200)
    return ('pin detail timeout', 400)

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
      
                return ('delete success', 200)
            return ('no this pin', 400)
        return ('need pin_id', 400)
    return ('del pin session timeout', 400)

@pin.route('/pins')
def show_pins():
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        pins = Pin.objects(owner=g.user_id)[:5].order_by('-create_at')
        res_data = pins_pack(pins, user)
        return (json.dumps(res_data), 200)
    return ('show_pins session timeout', 400)

@pin.route('/pins/before/<pin_id>')
def show_pins_before(pin_id):
    if g.user_id:
        time_tag = Pin.objects(id=pin_id).first().create_at
        user = User.objects(id=g.user_id).first()
        pins = Pin.objects(Q(create_at__lt=time_tag)&Q(owner=g.user_id))[:5].order_by('-create_at')
        res_data = pins_pack(pins, user)
        return (json.dumps(res_data), 200)
    return ('show_pins_before session timeout', 400)

@pin.route('/pins/user/<user_id>')
def show_pins_user(user_id):
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        pins = Pin.objects(owner=user_id)[:5].order_by('-create_at')
        res_data = pins_pack(pins, user)
        response = make_response(json.dumps(res_data))
        return response
    return ('show_pins session timeout', 400)

@pin.route('/pins/user/<user_id>/before/<pin_id>')
def show_pins_user_before(user_id, pin_id):
    if g.user_id:
        time_tag = Pin.objects(id=pin_id).first().create_at
        user = User.objects(id=g.user_id).first()
        pins = Pin.objects(Q(create_at__lt=time_tag)&Q(owner=user_id))[:5].order_by('-create_at')
        res_data = pins_pack(pins, user)
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

@pin.route('/likes/pin/<pin_id>', defaults={'page_num':1})
@pin.route('/likes/pin/<pin_id>/page/<int:page_num>')
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
            like_item['nickname'] = like.nickname
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
          <p>
             类型
             <input type=text name=type>
          <p>
             文本内容
             <input type=text name=content>
          <p>
             图片URL
             <input type=text name=pic>
          <p>
             <input type=submit value="发布">
        </form>    
        """
    return redirect(url_for('web.web_login'))







