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
        pin_item['price'] = pin.price
        pin_item['currency'] = pin.currency
        pin_item['stamp'] = pin.stamp
        pin_item['owner_desc'] = pin.owner_desc
        pin_item['comments_count'] = pin.comments_count
        pin_item['loc'] = pin.loc
        pin_item['geotag'] = pin.geotag_title
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

        pin_type = request.form['type'] if ('type' in request.form) and request.form['type'] else 1
        content = request.form['content'] if 'content' in request.form else ''
        pic = request.form['pic'] if 'pic' in request.form else ''
        stamp = request.form['stamp'] if ('stamp' in request.form) and request.form['stamp'] else 1
        price = float(request.form['price']) if 'price' in request.form else 1.0
        currency = request.form['currency'] if ('currency' in request.form) and request.form['currency'] else 'CNY'
        owner_desc = request.form['owner_desc'] if 'owner_desc' in request.form else None
        long = float(request.form['long']) if 'long' in request.form and request.form['long'] else None
        lat = float(request.form['lat']) if 'lat' in request.form and request.form['lat'] else None
        loc = [long, lat] if long and lat else None
        geotag_title = request.form['geotag'] if 'geotag' in request.form and request.form['geotag'] else None

        # ex_rate = request.form['ex_rate'] if 'ex_rate' in request.form else 1.0

        owner = User.objects(id=g.user_id).first()
        pin = Pin(type=pin_type,
                  content=content,
                  pic=pic,
                  stamp=stamp,
                  price=price,
                  currency=currency,
                  owner_desc=owner_desc,
                  owner=owner,
                  create_at=datetime.utcnow(),
                  avatar=owner.avatar,
                  loc=loc,
                  geotag_title=geotag_title)
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
            'pic':pin.pic,
            'stamp':pin.stamp,
            'currency':pin.currency,
            'price':pin.price,
            'owner_desc':pin.owner_desc,
            'owner_id':str(pin.owner.id),
            'loc':pin.loc,
            'geotag':pin.geotag_title,
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
        pin_item['price'] = pin.price
        pin_item['currency'] = pin.currency
        pin_item['stamp'] = pin.stamp
        pin_item['owner_desc'] = pin.owner_desc
        pin_item['loc'] = pin.loc
        pin_item['geotag'] = pin.geotag_title
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
        if user in pin.likes:
            pin.update(pull__likes=user, inc__likes_count=-1)
            return ('unlike success', 200)
        return ('not like this pin', 400)
    return ('unlike pin session timeout', 400)

@pin.route('/likes/pin/<pin_id>', defaults={'page_num':1})
@pin.route('/likes/pin/<pin_id>/page/<int:page_num>')
def pin_likes(pin_id, page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        pin = Pin.objects(id=pin_id).fields(slice__likes=[offset, limit]).first()
        user = User.objects(id=g.user_id).first()

        like_list = []
        for like in pin.likes:
            like_item = {}
            like_item['isfollowed'] = 1 if user in like.fans else 0
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
             价格
             <input type=text name=price>
          <p>
             货币类型（留空为人民币‘CNY’）
             <input type=text name=currency>
          <p>
             徽章（整型，留空为1）
             <input type=text name=stamp>
          <p>
             作者描述（可以留空）
             <input type=text name=owner_desc>
          <p>
             图片URL
             <input type=text name=pic>
          <p>
             地理标签
             <input type=text name=geotag>
          <p>
             经度
             <input type=text name=long>
          <p>
             维度
             <input type=text name=lat>
          <p>
             <input type=submit value="发布">
        </form>    
        """
    return redirect(url_for('web.web_login'))







