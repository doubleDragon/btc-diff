#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_blueprint(app)
    return app


def register_blueprint(app):
    from app.core.views import bp
    app.register_blueprint(bp)
    # from app.core.api import api
    # app.register_blueprint(api, url_prefix='/api')
