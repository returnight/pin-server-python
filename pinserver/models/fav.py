# -*- coding: utf-8 -*-
"""
    fav.py
    ~~~~~~~~~~~~~
    
    Pinserver Models Fav

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
"""

from pinserver.extensions import db

from pinserver.models.pin import Pin
from pinserver.models.user import User

class Fav(db.Document):
    """
        Favourite
        ~~~~~~~~~~

    """

    meta = {
        'collection':'favs',
        'ordering':['-create_at'],
    }

    owner = db.ReferenceField(User)
    pin = db.ReferenceField(Pin)
    create_at = db.DateTimeField()
