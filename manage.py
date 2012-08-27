# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~~
    
    Manage Pinserver
    
    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
"""

from flask.ext.script import Manager, Server
from pinserver import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

if __name__ == "__main__":
    manager.run()