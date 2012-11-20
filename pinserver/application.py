# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~~~~~
    
    Pinserver Application

    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe

    先不用急着拆分逻辑

    导入顺序
    --------

        #. 导入标准库

        #. 导入所需第三方库

        #. 导入flask库

        #. 导入flask ext库

        #. 导入项目辅助工具

        #. 导入项目包（model、view）

    函数顺序
    --------

        #. 辅助函数

        #. before_request

        #. teardown_request

        #. 各种路由

        #. GET POST要分开写

    依赖库
    --------
    bcrypt需要gcc和python-dev
    psycopg2需要libpq-dev    
    
    Session
    ---------
    
    # 此参数当写入session时配置
    session.permanent = True

"""

from flask import Flask

from pinserver import blueprints
from pinserver import extensions

from pinserver.config import DefaultConfig

__all__ = ['create_app']

DEFAULT_APP_NAME = 'pinserver'

DEFAULT_BLUEPRINTS = (
    (blueprints.user, ''),
    (blueprints.pin, ''),
    (blueprints.comment, ''),
    (blueprints.timeline, ''),
    (blueprints.relation, ''),
    (blueprints.fav, ''),
    (blueprints.geotag, ''),
    (blueprints.notice, ''),
    (blueprints.upload, ''),
    (blueprints.admin, ''),
    (blueprints.web, ''),
)

def create_app(config=None, app_name=None, blueprints=None):
    
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)

    configure_app(app, config)

    #TODO
    # config log
    # config error


    configure_extensions(app)

    configure_blueprints(app, blueprints)

    legacy(app)

    return app



def configure_app(app, config):

    app.config.from_object(DefaultConfig())

    if config:
        app.config.from_object(config)

    app.config.from_envvar('PIN_SERVER_SETTINGS', silent=True)



def configure_blueprints(app, blueprints):
    """
    register blueprints
    """
    for blueprint, url_prefix in blueprints:
        if url_prefix:
            app.register_blueprint(blueprint, url_prefix=url_prefix)
        else:
            app.register_blueprint(blueprint)

def configure_extensions(app):
    extensions.bcrypt.init_app(app)
    extensions.db.init_app(app)
    extensions.mongo.init_app(app)

def legacy(app):

    @app.route('/')
    def index():
        return 'Hello world'

    @app.template_filter('user_datetime')
    def user_datetime(datetime):
        return datetime.strftime('%Y-%m-%d @ %H:%M:%S')
    

