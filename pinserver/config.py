# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~~~~~
    
    Pinserver Config

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe

"""

class DefaultConfig(object):
    """
    Default configuration for Pin-server
    """
    
    SECRET_KEY = '>{O\xcfx\xa2>\xd8uf4\xe9-\xe8.N\n\x91\xea\xdcV\xbaNb'
    
    # for mongoengine
    MONGODB_DB = 'pinserver'

    # for pymongo
    MONGO_DBNAME = 'pinserver'
    
    UPLOAD_FOLDER = '/var/virenvs/pin-server/pinserver/pinserver/static'
    
    FILE_URL = 'http://testapi.get-pin.com/static/%s'
    
    AVATAR_UPLOAD_FOLDER = '/var/virenvs/pin-server/pinserver/pinserver/static/avatar'
    
    AVATAR_URL = 'http://testapi.get-pin.com/static/avatar/%s'
    
    # 3600*24*31 = 2678400
    PERMANENT_SESSION_LIFETIME = 2678400
    
class TestConfig(object):
    """
    For test
    """

    TESTING = True
    
    #TODO