# -*- coding: utf-8 -*-
"""
    timeline.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints timeline

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

import ujson as json
from mongoengine import Q

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import g

from flask.views import MethodView

from pinserver.helpers import before_request
from pinserver.models.timeline import Timeline

timeline = Blueprint('timeline', __name__)

timeline.before_request(before_request)

#support functions
def timeline_pack(timelines):
    timeline_list = []
    for timeline in timelines:
        timeline_item = {}
        timeline_item['tl_id'] = str(timeline.id)
        timeline_item['pin_id'] = str(timeline.pin.id)
        timeline_item['author'] = timeline.pin.owner.nickname
        timeline_item['content'] = timeline.pin.content
        timeline_item['avatar'] = timeline.pin.avatar
        timeline_item['create_at'] = timeline.create_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        timeline_list.append(timeline_item)
    res_data = {
        'total':len(timeline_list),
        'items':timeline_list,
    }
    return res_data

@timeline.route('/timeline')
def show_timeline():
    if g.user_id:
        timelines = Timeline.objects(owner=g.user_id)[:5].order_by('-create_at')
        res_data = timeline_pack(timelines)
        return (json.dumps(res_data), 200)
    return ('timeline session timeout', 400)

@timeline.route('/timeline/before/<timeline_id>')
def show_timeline_before(timeline_id):
    if g.user_id:
        time_tag = Timeline.objects(id=timeline_id).first().create_at
        timelines = Timeline.objects(Q(create_at__lt=time_tag)&Q(owner=g.user_id))[:5].order_by('-create_at')
        res_data = timeline_pack(timelines)
        return (json.dumps(res_data), 200)
    return ('timeline_before session timeout', 400)


