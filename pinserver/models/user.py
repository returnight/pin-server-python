# -*- coding: utf-8 -*-
"""
    user.py
    ~~~~~~~~~~~~~
    
    Pinserver Models User

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from pinserver import db

# models
class User(db.Document):
    """
        User
        ~~~~


    """
    meta = {'collection':'users'}

    email = db.EmailField(required=True, unique=True)
    password = db.StringField(max_length=64, required=True)
    nickname = db.StringField(max_length=32, required=True)
    register_at = db.DateTimeField(default=datetime.utcnow(), required=True)
    avatar = db.StringField(max_length=256)
    
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

