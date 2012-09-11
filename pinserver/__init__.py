# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~
    
    Pinserver Main

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
    
    :author: Guo Peng (G_will) <g_will@ieqi.com> 
    :copyright: (c) 2012-2012 by Swipppe
    
    
    Session
    ---------
    
    # 此参数当写入session时配置
    session.permanent = True

"""

from pinserver.application import create_app
