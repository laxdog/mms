# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'libs/x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css'
    'css/style.css',
    filters='cssmin',
    output='public/css/common.css'
)

js = Bundle(
    'libs/jQuery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'libs/x-editable/dist/bootstrap3-editable/js/bootstrap-editable.js'
    'js/plugins.js',
    filters='jsmin',
    output='public/js/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
