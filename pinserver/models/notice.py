# -*- coding: utf-8 -*-
"""
    notice.py
    ~~~~~~~~~~~~~
    
    Pinserver Models Notice

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from pinserver.extensions import db

from pinserver.models.user import User

class Notice(db.Document):
    """
        Notice
        ~~~~~~~~

        通知

    """

    meta = {
        'collection':'notices',
        'ordering':['-create_at'],
    }
    nt_type = db.IntField()
    content = db.StringField()
    owner = db.ReferenceField(User)
    create_at = db.DateTimeField()
