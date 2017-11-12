#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import render_template

from app import app
from app.tools import utils


@app.route('/')
@app.route('/diff')
def index():
    ticker = utils.get_diff()

    return render_template('diff.html', ticker=ticker)
