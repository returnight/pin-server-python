# -*- coding: utf-8 -*-
"""
    geotag.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints Geotag

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

import ujson as json
from datetime import datetime
from mongoengine import Q

from flask import Blueprint
from flask import g
from flask import request
from flask import redirect
from flask import url_for

from pinserver.helpers import before_request
from pinserver.models.user import User
from pinserver.models.geotag import Geotag

geotag = Blueprint('geotag', __name__)

geotag.before_request(before_request)

# support functions
def geotags_pack(geotags):
    geotags_list = []
    for geotag in geotags:
        geotag_item = {}
        geotag_item['geotag_id'] = str(geotag.id)
        geotag_item['title'] = geotag.title
        geotag_item['loc'] = geotag.loc
        geotags_list.append(geotag_item)
    res_data = {
        'total':len(geotags_list),
        'items':geotags_list,
    }
    return res_data

@geotag.route('/geotag', methods=['POST'])
def geotag_post():
    if g.user_id:
        
        long = float(request.form['long']) if 'long' in request.form else None
        lat = float(request.form['lat']) if 'lat' in request.form else None
        title = request.form['title'] if 'title' in request.form else ''
        owner = User.objects(id=g.user_id).first()

        geotag = Geotag(title=title,
                        owner=owner,
                        loc=[long,lat],
                        create_at=datetime.utcnow())
        geotag.save()

        geotag_item = {
            'geotag_id':str(geotag.id),
            'title':geotag.title,
            'loc':geotag.loc,
            'create_at':geotag.create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }

        return (json.dumps(geotag_item), 200)
    return ('post geotag session timeout', 400)

@geotag.route('/geotags/long/<float:long>/lat/<float:lat>', defaults={'query':None, 'page_num':1})
@geotag.route('/geotags/long/<float:long>/lat/<float:lat>/page/<int:page_num>', defaults={'query':None})
@geotag.route('/geotags/long/<float:long>/lat/<float:lat>/q/<query>', defaults={'page_num':1})
@geotag.route('/geotags/long/<float:long>/lat/<float:lat>/q/<query>/page/<int:page_num>')
def geotags(long, lat, query, page_num):
    if g.user_id:
        limit = 5
        start = (page_num - 1) * limit
        end = page_num * limit
        if query:
            geotags = Geotag.objects(Q(loc__within_distance=[(long, lat), 5]) & Q(title__contains=query))[start:end]
        else:    
            geotags = Geotag.objects(loc__within_distance=[(long, lat), 5])[start:end]
        res_data = geotags_pack(geotags)
        return (json.dumps(res_data), 200)
    return ('geotags session timeout', 400)

@geotag.route('/web/geotag')
def web_geotag():
    if g.user_id:
        return """
        <!doctype html>
        <title>发布Geotag</title>
        <h1>发布Geotag</h1>
        <form action="/geotag" method=post>
          <p>
             标题
             <input type=text name=title>
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
