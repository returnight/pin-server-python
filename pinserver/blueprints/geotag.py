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

        # lat = request.form['lat'] if ('lat' in request.form) and request.form['lat'] else 1
        # long = request.form['long'] if 'long' in request.form else ''
        # pic = request.form['pic'] if 'pic' in request.form else ''
        # stamp = request.form['stamp'] if ('stamp' in request.form) and request.form['stamp'] else 1
        # price = float(request.form['price']) if 'price' in request.form else 1.0
        # currency = request.form['currency'] if ('currency' in request.form) and request.form['currency'] else 'CNY'

        lat = float(request.form['lat']) if 'lat' in request.form else None
        long = float(request.form['long']) if 'long' in request.form else None
        title = request.form['title'] if 'title' in request.form else ''
        owner = User.objects(id=g.user_id).first()

        geotag = Geotag(title=title,
                        owner=owner,
                        loc=[lat,long])
        geotag.save()

        geotag_item = {
            'geotag_id':str(geotag.id),
            'loc':geo.loc,
            'create_at':pin.create_at.strftime('%Y-%m-%d %H:%M:%S'),
            }

        return (json.dumps(geotag_item), 200)
    return ('post geotag session timeout', 400)

@geotag.route('/geotags/lat/<float:lat>/long/<float:long>')
def geotags(lat, long):
    if g.user_id:
        geotags = Geotag.objects(loc__near=[lat, long])[:5]
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
             <input type=text name=lat>
          <p>
             维度
             <input type=text name=long>
          <p>
             <input type=submit value="发布">
        </form>    
        """
    return redirect(url_for('web.web_login'))
