# -*- coding: utf-8 -*-
"""
    fav.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints fav

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

import ujson as json
from datetime import datetime

from flask import Blueprint
from flask import g

from pinserver.helpers import before_request
from pinserver.models.user import User
from pinserver.models.pin import Pin
from pinserver.models.fav import Fav

fav = Blueprint('fav', __name__)

fav.before_request(before_request)

@fav.route('/fav/<pin_id>')
def fav_pin(pin_id):
    if g.user_id:
        already_fav = Fav.objects(owner=g.user_id, pin=pin_id).first()
        if not already_fav:
            pin = Pin.objects(id=pin_id).first()
            user = User.objects(id=g.user_id).first()
            fav = Fav(owner=user,
                      pin=pin,
                      create_at=datetime.utcnow())
            fav.save()
            return ('fav success', 200)
        return ('already fav', 400)
    return ('fav pin session timeout', 400)

@fav.route('/unfav/<pin_id>')
def unfav_pin(pin_id):
    if g.user_id:
        fav = Fav.objects(owner=g.user_id, pin=pin_id).first()
        if fav:
            fav.delete()
            return ('unfav success', 200)
        return ('no this fav', 400)    
    return ('unfav session timeout', 400)

@fav.route('/favs', defaults={'page_num':1})
@fav.route('/favs/page/<int:page_num>')
def favs_mine(page_num):
    if g.user_id:
        limit = 5
        start = (page_num - 1) * limit
        end = page_num * limit
        favs = Fav.objects(owner=g.user_id)[start:end].order_by('-create_at')

        fav_list = []
        for fav in favs:
            fav_item = {}
            fav_item['pin_id'] = str(fav.pin.id)
            fav_item['create_at'] = fav.create_at.strftime('%Y-%m-%d %H:%M:%S')
            fav_list.append(fav_item)
        res_data = {
            'total':len(fav_list),
            'items':fav_list,
        }

        return (json.dumps(res_data), 200)
    return ('favs mine session timeout', 400)
