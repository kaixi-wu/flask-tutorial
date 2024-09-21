# -*- coding: utf-8 -*-
from flask import Flask
from utils.json_util import CustomJSONEncoder
from utils.views import restful
from base_model import db
from hooks.before_request import register_before_hooks

import os
import config


def create_app(test_config=None):
    # create app and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(config)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    # 绑定app到数据库实例
    db.init_app(app)
    app.restful = restful
    # migrate.init_app(app, db)

    register_before_hooks(app)

    # 测试数据库连接
    # with app.app_context() as ap:
    #     with db.engine.connect() as conn:
    #         rs = conn.execute(text("select now() as curl_time from dual")).fetchone()
    #         if rs is not None:
    #             print("database connect is success!!")

    # 注册蓝图
    from auth.blueprint import auth_blue
    from business.blueprint import business_blue
    app.register_blueprint(blueprint=auth_blue, url_prefix="/user")
    app.register_blueprint(blueprint=business_blue, url_prefix='/business')
    app.add_url_rule('/error', endpoint='index')

    return app
