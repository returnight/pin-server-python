# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~~~~~~~~
    
    Pinserver Blueprints admin

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    

"""

from flask import Blueprint
from flask import render_template

admin = Blueprint('admin', pinserver)

@admin.route('/')
def admin_index():
    return render_template('admin/index.html')

    