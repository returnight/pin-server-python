# -*- coding: utf-8 -*-
"""
    geotag.py
    ~~~~~~~~~~~~~
    
    Pinserver Models Geotag

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from pinserver.extensions import db

from pinserver.models.user import User

class Geotag(db.Document):
    """
        Geo Tag
        ~~~~~~~~~~

        地理位置标签

        loc:[lat, long]
        lat:经度
        long:维度

    """

    meta = {
        'collection':'geotags',
        'ordering':['-create_at'],
        # 'indexes': ['*loc.point'],
    }

    title = db.StringField()
    owner = db.ReferenceField(User)
    loc = db.GeoPointField()
    create_at = db.DateTimeField()
