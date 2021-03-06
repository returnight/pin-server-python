# -*- coding: utf-8 -*-
"""
    helper.py
    ~~~~~~~~~~~~~
    
    Pinserver Helpers

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe

"""

import time

from flask import g
from flask import session


def before_request():
    """
    每次请求前从session中提出用户信息
    """
    g.user_id = None
    if 'user_id' in session:
        g.user_id = session['user_id']
        
def timestamp(date_time):
    """
    从datetime获取时间戳
    """
    return int(time.mktime(date_time.timetuple()))