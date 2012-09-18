# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~~
    
    Manage Pinserver
    
    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
"""

import pymongo

from flask.ext.script import Manager, Server

from pinserver import create_app


app = create_app()

manager = Manager(app)

db_name = app.config['MONGODB_DB']

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

@manager.command
def drop_db():
    conn = pymongo.Connection()
    conn.drop_database(db_name)
    print 'Drop DB Done.'

if __name__ == "__main__":
    manager.run()