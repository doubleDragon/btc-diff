#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import render_template, Blueprint

from app.tools import utils

bp = Blueprint('diff', __name__)


@bp.route('/')
@bp.route('/diff')
def index():
    ticker = utils.get_diff()

    return render_template('diff.html', ticker=ticker)
