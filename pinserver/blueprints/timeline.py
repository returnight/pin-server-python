# -*- coding: utf-8 -*-
"""
    timeline.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints timeline

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

import ujson as json

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import g

from flask.views import MethodView

from pinserver.helpers import before_request
from pinserver.models.timeline import Timeline

timeline = Blueprint('timeline', __name__)

timeline.before_request(before_request)

#TODO
@timeline.route('/timeline')
def show_timeline():
    if g.user_id:
        timelines = Timeline.objects(owner=g.user_id)[:5].order_by('-create_at')
        timeline_list = []
        for timeline in timelines:
            timeline_item = {}
            timeline_item['author'] = timeline.pin.owner.nickname
            timeline_item['content'] = timeline.pin.content
            timeline_item['avatar'] = timeline.pin.avatar
            timeline_item['create_at'] = timeline.create_at.strftime('%Y-%m-%d %H:%M:%S.%f')
            timeline_list.append(timeline_item)
        res_data = {
            'total':len(timeline_list),
            'items':timeline_list,
        }
        return (json.dumps(res_data), 200)
    else:
        return ('timeline session timeout', 400)

# @timeline.route('/timeline/<user_id>')
# def show_user_timeline(user_id):
#     timelines = Timeline.objects(owner=user_id)

