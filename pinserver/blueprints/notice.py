# -*- coding: utf-8 -*-
"""
    notice.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints Notice

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2013 by Swipppe
    

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
from pinserver.models.notice import Notice

notice = Blueprint('notice', __name__)

notice.before_request(before_request)

# support functions
def notices_pack(notices):
    notices_list = []
    for notice in notices:
        notice_item = {}
        notice_item['id'] = str(notice.id)
        notice_item['type'] = notice.notice_type
        notice_item['content'] = notice.content
        notice_item['owner'] = str(notice.owner.id)
        notice_item['create_at'] = notice.create_at.strftime('%Y-%m-%d %H:%M:%S')
        notices_list.append(notice_item)
    res_data = {
        'total':len(notices_list),
        'items':notices_list,
    }
    return res_data

@notice.route('/notices', defaults={'page_num':1})
@notice.route('/notices/page/<int:page_num>')
def show_notices(page_num):
    if g.user_id:
        limit = 5
        start = (page_num - 1) * limit
        end = page_num * limit
        notices = Notice.objects(readed=False).order_by('-create_at')
        res_data = notices_pack(notices)
        return (json.dumps(res_data), 200)
    return ('show notices session timeout', 400)

@notice.route('/notice/read/<notice_id>')
def read_notice(notice_id):
    if g.user_id:
        notice = Notice.objects(id=notice_id).first()
        notice.readed = True
        notice.save()
        return ('read notice success', 200)
    return ('read notice session timeout', 400)

# for test
@notice.route('/notice', methods=['POST'])
def post_notice():
    if g.user_id:
        notice_type = request.form['type']
        content = request.form['content']
        owner = User.objects(id=g.user_id).first()
        notice = Notice(notice_type=notice_type,
                        content=content,
                        owner=owner,
                        create_at=datetime.utcnow())
        notice.save()
        notice_item = {
            'id':str(notice.id),
            'type':notice.notice_type,
            'content':notice.content,
            'create_at':notice.create_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return (json.dumps(notice_item), 200)
    return ('post notice session timeout', 400)

@notice.route('/web/notice')
def web_notice():
    if g.user_id:
        return """
        <!doctype html>
        <title>添加通知</title>
        <h1>add notice</h1>
        <form action="/notice" method=post>
          <p>
             类型
             <input type=text name=type>
          <p>
             文本内容
             <input type=text name=content>
          <p>
             <input type=submit value="添加">
        </form>      
        """
    return redirect(url_for('web.web_login'))
