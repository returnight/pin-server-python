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
    
    MONGODB_DB = 'pinserver'
    
    UPLOAD_FOLDER = '/var/virenvs/pin-server/pinserver/pinserver/static/img/avatar'
    
    AVATAR_URL = 'http://testapi.get-pin.com/static/img/avatar/%s'
    
    PERMANENT_SESSION_LIFETIME = 120
    
class TestConfig(object):
    """
    For test
    """

    TESTING = True
    
    #TODO