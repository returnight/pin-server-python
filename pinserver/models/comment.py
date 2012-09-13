# -*- coding: utf-8 -*-
"""
    comment.py
    ~~~~~~~~~~~~~
    
    Pinserver Models Comment

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from pinserver.extensions import db
from pinserver.models.user import User
from pinserver.models.pin import Pin

class Comment():
    """
        Comment
        ~~~~~~~~

    """

    meta = {
        'collection':'comments',
        'ordering':['-create_at'],
    }

    content = db.StringField()
    author = db.ReferenceField(User)
    pin = db.ReferenceField(Pin)
    create_at = db.DateTimeField()
