# -*- coding: utf-8 -*-
"""
    timeline.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints timeline

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

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
@timeline.route('/timeline', defaults={'user_id':''})
def show_timeline(user_id):
	if g.user_id:
		return jsonify(user_id=g.user_id)
	else:
		err_msg = 'session timeout'
		return jsonify(err_msg=err_msg)

@timeline.route('/timeline/<user_id>')
def show_user_timeline(user_id):
	timelines = Timeline.objects(owner.id=user_id).all()

