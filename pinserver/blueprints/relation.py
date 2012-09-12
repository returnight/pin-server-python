# -*- coding: utf-8 -*-
"""
    relation.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints relation

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

relation = Blueprint('relation', __name__)

relation.before_request(before_request)

#support functions
def followers_pack(followers):
    follower_list = []
    for follower in followers:
        follower_item = {}
        follower_item['user_id'] = str(follower.id)
        follower_item['nickname'] = follower.nickname
        follower_item['avatar'] = follower.avatar
        follower_list.append(follower_item)
    res_data = {
        'total':len(follower_list),
        'items':follower_list,
    }
    return res_data

def fans_pack(fans):
    fan_list = []
    for fan in fans:
        fan_item = {}
        fan_item['user_id'] = str(fan.id)
        fan_item['nickname'] = fan.nickname
        fan_item['avatar'] = fan.avatar
        fan_list.append(fan_item)
    res_data = {
        'total':len(fan_list),
        'items':fan_list,
    }
    return res_data

@relation.route('/relation/follow/<user_id>')
def relation_follow(user_id):
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        follower = User.objects(id=user_id).first()
        User.objects(id=g.user_id).update_one(push__followers=follower, inc__followers_count=1)
        User.objects(id=user_id).update_one(push__fans=user, inc__fans_count=1)

        return ('follow success', 200)
    return ('relation follow session timeout', 401)

@relation.route('/relation/unfollow/<user_id>')
def relation_unfollow(user_id):
    if g.user_id:
        user = User.objects(id=g.user_id).first()
        follower = User.objects(id=user_id).first()
        User.objects(id=g.user_id).update_one(pull__followers=follower, inc__followers_count=-1)
        User.objects(id=user_id).update_one(pull__fans=user, inc__fans_count=-1)

@relation.route('/relation/followers', defaults={'page_num':1})
@relation.route('/relation/followers/page/<int:page_num>')
def relation_followers(page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        user = User.objects(id=g.user_id).fields(slice__followers=[offset, limit])
        followers = user.followers
        res_data = followers_pack(followers)
        return (json.dumps(res_data), 200)
    return ('followers list session timeout', 400)

@relation.route('/relation/fans', defaults={'page_num':1})
@relation.route('/relation/fans/page/<int:page_num>')
def relation_fans(page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        fans = User.objects(id=g.user_id).fields(slice__fans=[offset, limit])

        res_data = fans_pack(fans)
        return (json.dumps(res_data), 200)
    return ('fans list session timeout', 400)
