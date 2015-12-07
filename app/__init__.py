# coding=utf-8

from os import urandom
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = urandom(24)
	
    # 注册蓝本
    from .news import news as news_blueprint
    app.register_blueprint(news_blueprint)

    from .query import query as query_blueprint
    app.register_blueprint(query_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .kebiao import kebiao as kebiao_blueprint
    app.register_blueprint(kebiao_blueprint)

    from .repair import repair as repair_blueprint
    app.register_blueprint(repair_blueprint)

    return app
