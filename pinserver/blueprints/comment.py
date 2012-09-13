# -*- coding: utf-8 -*-
"""
    comment.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints comment

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
from pinserver.models.comment import Comment


comment = Blueprint('comment', __name__)

comment.before_request(before_request)

# support functions
def comments_pack(comments):
    comment_list = []
    for comment in comments:
        comment_item = {}
        comment_item['comment_id'] = str(comment.id)
        comment_item['content'] = comment.content
        comment_item['author_id'] = str(comment.author.id)
        comment_item['author_name'] = comment.author.nickname
        comment_item['create_at'] = comment.create_at.strftime('%Y-%m-%d %H:%M:%S')
        comment_list.append(comment_item)
    res_data = {
        'total':len(comment_list),
        'items':comment_list,
    }
    return res_data


@comment.route('/comment/pin/<pin_id>', methods=['POST'])
def comment_pin(pin_id):
    if g.user_id:
        content = request.form['content']
        user = User.objects(id=g.user_id).first()
        pin = Pin.objects(id=pin_id).first()
        comment = Comment(content=content,
                          author=user,
                          pin=pin,
                          create_at=datetime.utcnow())
        comment.save()
        pin.update(inc__comments_count=1)
        return ('comment pin success', 200)
    return ('comment pin session timeout', 400)

@comment.route('/del_comment/<comment_id>')
def del_comment(comment_id):
    if g.user_id:
        comment = Comment.objects(id=comment_id).first()
        comment.pin.update(inc__comments_count=-1)
        comment.delete()
        return ('del comment success', 200)
    return ('del comment session timeout', 400)

@comment.route('/comments/pin/<pin_id>', defaults={'page_num':1})
@comment.route('/comments/pin/<pin_id>/page/<int:page_num>')
def comments_pin(pin_id, page_num):
    if g.user_id:
        limit = 5
        start = (page_num - 1) * limit
        end = page_num * limit
        comments = Comment.objects(pin=pin_id)[start:end].order_by('-create_at')
        res_data = comments_pack(comments)
        return (json.dumps(res_data), 200)
    return ('comments pin session timeout', 400)

@comment.route('/comments', defaults={'page_num':1})
@comment.route('/comments/page/<int:page_num>')
def comments_mine(page_num):
    if g.user_id:
        limit = 5
        start = (page_num - 1) * limit
        end = page_num * limit
        comments = Comment.objects(author=g.user_id)[start:end].order_by('-create_at')
        res_data = comments_pack(comments)
        return (json.dumps(res_data), 200)
    return ('comments mine session timeout', 400)

@comment.route('/comments/user/<user_id>', defaults={'page_num':1})
@comment.route('/comments/user/<user_id>/page/<int:page_num>')
def comments_mine(user_id, page_num):
    if g.user_id:
        limit = 5
        start = (page_num - 1) * limit
        end = page_num * limit
        comments = Comment.objects(author=user_id)[start:end].order_by('-create_at')
        res_data = comments_pack(comments)
        return (json.dumps(res_data), 200)
    return ('comments mine session timeout', 400)

