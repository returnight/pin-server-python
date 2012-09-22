# -*- coding: utf-8 -*-
"""
    pin.py
    ~~~~~~~~~~~~~
    
    Pinserver Models Pin

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from datetime import datetime

from pinserver.extensions import db
from pinserver.models.user import User

class Pin(db.Document):
    """
        Pin
        ~~~~


    """
    meta = {
        'collection':'pins',
        'ordering':['-create_at'],
    }

    #type 需要约定
    type = db.IntField()
    content = db.StringField()
    owner = db.ReferenceField(User)
    create_at = db.DateTimeField()
    avatar = db.StringField()

    pic = db.StringField()

    stamp = db.IntField()

    price = db.FloatField()
    currency = db.StringField()

    ex_rate = db.FloatField(default=1.0)

    likes_count = db.IntField(default=0)
    likes = db.ListField(db.ReferenceField(User))

    comments_count = db.IntField(default=0)

    first_comment = db.StringField()
    first_comment_user = db.ReferenceField(User)
    first_comment_create_at = db.DateTimeField()

    last_comment = db.StringField()
    last_comment_user = db.ReferenceField(User)
    last_comment_create_at = db.DateTimeField()

    # 地理  经，纬 [x, y]
    # loc = db.ListField()
    
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
