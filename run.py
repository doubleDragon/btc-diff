#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# from app import app
#
# app.run(host='0.0.0.0')

from app import create_app

if __name__ == '__main__':
    app = create_app()

    app.run(host='0.0.0.0')
    # app.run(debug=True)
