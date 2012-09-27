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
def followers_pack(followers, user):
    follower_list = []
    for follower in followers:
        follower_item = {}
        follower_item['user_id'] = str(follower.id)
        follower_item['nickname'] = follower.nickname
        follower_item['avatar'] = follower.avatar
        follower_item['isfollowed'] = 1 if user in follower.fans else 0
        follower_list.append(follower_item)
    res_data = {
        'total':len(follower_list),
        'items':follower_list,
    }
    return res_data

def fans_pack(fans, user):
    fan_list = []
    for fan in fans:
        fan_item = {}
        fan_item['user_id'] = str(fan.id)
        fan_item['nickname'] = fan.nickname
        fan_item['avatar'] = fan.avatar
        fan_item['isfollowed'] = 1 if user in fan.fans else 0
        fan_list.append(fan_item)
    res_data = {
        'total':len(fan_list),
        'items':fan_list,
    }
    return res_data

@relation.route('/relation/follow/<user_id>')
def relation_follow(user_id):
    if g.user_id:

        follower = User.objects(id=user_id).first()
        user = User.objects(id=g.user_id, followers__nin=[follower]).first()
        if user:
        
            #TODO need optim
            # user.update(***)
            User.objects(id=g.user_id).update_one(push__followers=follower, inc__followers_count=1)
            User.objects(id=user_id).update_one(push__fans=user, inc__fans_count=1)

            return ('follow success', 200)
        return ('already followed', 400)
    return ('relation follow session timeout', 401)

@relation.route('/relation/unfollow/<user_id>')
def relation_unfollow(user_id):
    if g.user_id:
        follower = User.objects(id=user_id).first()
        user = User.objects(id=g.user_id).first()
        User.objects(id=g.user_id).update_one(pull__followers=follower, inc__followers_count=-1)
        User.objects(id=user_id).update_one(pull__fans=user, inc__fans_count=-1)
        return ('unfollow success', 200)
    return ('unfollow session timeout', 400)

@relation.route('/relation/followers', defaults={'page_num':1})
@relation.route('/relation/followers/page/<int:page_num>')
def relation_followers(page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        user = User.objects(id=g.user_id).fields(slice__followers=[offset, limit]).first()
        followers = user.followers
        res_data = followers_pack(followers, user)
        return (json.dumps(res_data), 200)
    return ('followers list session timeout', 400)

@relation.route('/relation/fans', defaults={'page_num':1})
@relation.route('/relation/fans/page/<int:page_num>')
def relation_fans(page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        user = User.objects(id=g.user_id).fields(slice__fans=[offset, limit]).first()
        fans = user.fans
        res_data = fans_pack(fans, user)
        return (json.dumps(res_data), 200)
    return ('fans list session timeout', 400)

@relation.route('/relation/user/<user_id>/followers', defaults={'page_num':1})
@relation.route('/relation/user/<user_id>/followers/page/<int:page_num>')
def relation_user_followers(user_id, page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        user = User.objects(id=user_id).fields(slice__followers=[offset, limit]).first()
        followers = user.followers
        res_data = followers_pack(followers, user)
        return (json.dumps(res_data), 200)
    return ('followers list session timeout', 400)

@relation.route('/relation/user/<user_id>/fans', defaults={'page_num':1})
@relation.route('/relation/user/<user_id>/fans/page/<int:page_num>')
def relation_user_fans(user_id, page_num):
    if g.user_id:
        limit = 5 
        offset = (page_num - 1) * limit
        user = User.objects(id=user_id).fields(slice__fans=[offset, limit]).first()
        fans = user.fans
        res_data = fans_pack(fans, user)
        return (json.dumps(res_data), 200)
    return ('fans list session timeout', 400)
