# -*- coding: utf-8 -*-
"""
    extensions.py
    ~~~~~~~~~~~~~~
    
    Pinserver Extensions

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe

"""

from flask.ext.bcrypt import Bcrypt
from flask.ext.mongoengine import MongoEngine
from flask.ext.pymongo import PyMongo

bcrypt = Bcrypt()
db = MongoEngine()
mongo = PyMongo()