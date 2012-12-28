# -*- coding: utf-8 -*-
"""
    user.py
    ~~~~~~~~~~~~~
    
    Pinserver Models User

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from datetime import datetime

from pinserver.extensions import db

# models
class User(db.Document):
    """
        User
        ~~~~


    """
    meta = {'collection':'users'}

    email = db.EmailField(unique=True, required=False)
    password = db.StringField(max_length=64)
    nickname = db.StringField(max_length=32)
    register_at = db.DateTimeField(default=datetime.utcnow())
    avatar = db.StringField(default='',max_length=256)

    weibo_id = db.StringField(unique=True)
    weibo_token = db.StringField()
    
    pins_count = db.IntField(default=0)

    followers = db.ListField(db.ReferenceField('self'))
    followers_count = db.IntField(default=0)

    fans = db.ListField(db.ReferenceField('self'))
    fans_count = db.IntField(default=0)

    favs_count = db.IntField(default=0)

    """
    username = db.StringField(max_length=32, unique=True)
    
    
    
    # 地理
    loc = db.ListField()
    
    # 绑定
    auth = db.ListField(db.EmbeddedDocumentField(Auth))
    
    
    # 0: 未知 1: 男 2: 女
    gender = db.IntField()
    currency = db.StringField(max_length=3)
    realname = db.StringField(max_length=32)
    birthday = db.DateTimeField()
    country = db.StringField(max_length=32)
    province = db.StringField(max_length=32)
    city = db.StringField(max_length=32)
    slogan = db.StringField()
    
    
    # 0: 未激活 1: 激活
    status = db.IntField(default=1)
    """

class Auth(db.EmbeddedDocument):
    """
        Auth
        ~~~~~


    """
    
    type = db.StringField()
    aid = db.StringField()
    token = db.StringField()

