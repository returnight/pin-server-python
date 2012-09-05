# -*- coding: utf-8 -*-
"""
    timeline.py
    ~~~~~~~~~~~~~
    
    Pinserver Models Timeline

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from datetime import datetime

from pinserver import db

from pinserver.models.user import User
from pinserver.models.pin import Pin

class Timeline(db.Document):
    """
        Pin
        ~~~~


    """
    meta = {
        'collection':'timeline',
        'ordering':['-create_at'],
    }

    pin = db.ReferenceField(Pin)
    owner = db.ReferenceField(User)
    create_at = db.DateTimeField(required=True)
    
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


