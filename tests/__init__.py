# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~
    
    Pinserver Tests
    
    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
"""

from flask import g
from flaskext.testing import TestCase as Base
from flaskext.testing import Twill
from flaskext.principal import identity_changed
from flaskext.principal import Identity
from flaskext.principal import AnonymousIdentity

